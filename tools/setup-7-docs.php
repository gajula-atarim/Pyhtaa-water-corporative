<?php
/**
 * Setup step 7 – copy the documents the pages link to (PDF/DOC on the old site pyhtaanvok.fi) into this
 * site's Media Library. Read-only towards the old site. Run in batches: define PV_DOC_FROM / PV_DOC_COUNT.
 * Already-copied files are skipped, so a batch can be re-run safely.
 * The map old URL => [attachment ID, new URL] is kept in the option pv_doc_map.
 */
if (!defined('PV_SRC')) exit('PV_SRC not defined');
$admins = get_users(array('role' => 'administrator', 'number' => 1, 'fields' => 'ID'));
if ($admins) wp_set_current_user((int) $admins[0]);
require_once ABSPATH . 'wp-admin/includes/file.php';
require_once ABSPATH . 'wp-admin/includes/media.php';
require_once ABSPATH . 'wp-admin/includes/image.php';
@set_time_limit(600);

$r = wp_remote_get(PV_SRC . 'tools/data/docs-to-migrate.json', array('timeout' => 30));
if (wp_remote_retrieve_response_code($r) !== 200) exit('fetch failed');
$urls = json_decode(wp_remote_retrieve_body($r), true);
$from = defined('PV_DOC_FROM') ? PV_DOC_FROM : 0;
$count = defined('PV_DOC_COUNT') ? PV_DOC_COUNT : 20;
$map = get_option('pv_doc_map', array());
$out = array('ok' => 0, 'skipped' => 0, 'failed' => array());

foreach (array_slice($urls, $from, $count) as $url) {
	if (!empty($map[$url][0]) && get_post($map[$url][0])) { $out['skipped']++; continue; }
	$tmp = download_url($url, 120);
	if (is_wp_error($tmp)) { $out['failed'][$url] = $tmp->get_error_message(); continue; }
	$name = rawurldecode(basename(parse_url($url, PHP_URL_PATH)));
	// keep the original upload month (…/2024/11/…) so the files stay organised the same way
	$time = preg_match('#/(\d{4})/(\d{2})/[^/]+$#', $url, $m) ? $m[1] . '/' . $m[2] : null;
	$id = media_handle_sideload(array('name' => $name, 'tmp_name' => $tmp), 0, null, array(), $time);
	if (is_wp_error($id)) { @unlink($tmp); $out['failed'][$url] = $id->get_error_message(); continue; }
	update_post_meta($id, '_pv_source_url', $url);
	$map[$url] = array($id, wp_get_attachment_url($id));
	update_option('pv_doc_map', $map, false); // save after every file, so a timeout never loses work
	$out['ok']++;
}
$out['total_mapped'] = count($map);
echo wp_json_encode($out);
