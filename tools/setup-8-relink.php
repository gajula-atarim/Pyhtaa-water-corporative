<?php
/**
 * Setup step 8 – point every document link at the copies in this site's Media Library.
 * Uses the pv_doc_map option written by setup-7-docs.php (old URL => [ID, new URL]) and rewrites the
 * Elementor data of the home page, the inner pages and the UAE header/footer. Only link strings change.
 */
if (!defined('PV_SRC')) exit('PV_SRC not defined');
$admins = get_users(array('role' => 'administrator', 'number' => 1, 'fields' => 'ID'));
if ($admins) wp_set_current_user((int) $admins[0]);

$map = get_option('pv_doc_map', array());
$from = array(); $to = array();
foreach ($map as $old => $v) {
	if (empty($v[1])) continue;
	$from[] = $old; $to[] = $v[1];
	$dec = rawurldecode($old); // the same link written with plain ä/ö
	if ($dec !== $old) { $from[] = $dec; $to[] = $v[1]; }
}
if (!function_exists("pv_relink")) { function pv_relink(&$node, $from, $to, &$n) {
	if (is_array($node)) { foreach ($node as &$c) pv_relink($c, $from, $to, $n); return; }
	if (is_string($node) && strpos($node, 'pyhtaanvok.fi/wp-content/uploads/sites/1503/') !== false) {
		$new = str_replace($from, $to, $node, $k);
		if ($k) { $node = $new; $n += $k; }
	}
} }
/* documents (PDF/DOC) open in a new tab: link controls get "Open in new window", inline <a> get target="_blank" */
if (!function_exists("pv_doc_newtab")) { function pv_doc_newtab(&$node, &$n) {
	if (!is_array($node)) return;
	if (isset($node['url']) && is_string($node['url']) && preg_match('/\.(pdf|docx?)(\?|#|$)/i', $node['url'])
		&& (!isset($node['is_external']) || $node['is_external'] !== 'on')) { $node['is_external'] = 'on'; $n++; }
	foreach ($node as $k => &$v) {
		if (is_string($v) && stripos($v, '<a ') !== false) {
			$new = preg_replace('/<a (?![^>]*target=)([^>]*href="[^"]+\.(?:pdf|docx?)"[^>]*)>/i', '<a $1 target="_blank" rel="noopener">', $v, -1, $k2);
			if ($k2) { $v = $new; $n += $k2; }
		} elseif (is_array($v)) {
			pv_doc_newtab($v, $n);
		}
	}
} }

$ids = array_merge(array(36), array_values(array_map('intval', get_option('pv_page_map'))), array(57, 59));
$rl_out = array();
foreach (array_unique($ids) as $id) {
	$raw = get_post_meta($id, '_elementor_data', true);
	if (!$raw) continue;
	$data = is_array($raw) ? $raw : json_decode($raw, true);
	if (!is_array($data)) { $rl_out[$id] = 'bad json'; continue; }
	$n = 0;
	pv_relink($data, $from, $to, $n);
	$t = 0;
	pv_doc_newtab($data, $t);
	if ($n || $t) {
		$doc = \Elementor\Plugin::$instance->documents->get($id, false);
		$doc->save(array('elements' => $data));
	}
	$left = substr_count(get_post_meta($id, '_elementor_data', true), 'uploads\/sites\/1503') + substr_count(get_post_meta($id, '_elementor_data', true), 'uploads/sites/1503');
	$rl_out[$id] = array('replaced' => $n, 'new_tab' => $t, 'old_links_left' => $left);
}
\Elementor\Plugin::$instance->files_manager->clear_cache();
wp_cache_flush();
echo wp_json_encode($rl_out);
