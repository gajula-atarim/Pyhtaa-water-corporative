<?php
/**
 * Setup step 4a – media for the inner pages (run with the same WP-CLI loader as the other steps).
 * Imports the new SVG icons and photos into the Media Library (skips anything already imported)
 * and prints the media map that tools/data/site.json needs.
 */
if (!defined('PV_SRC')) exit('PV_SRC not defined');
$out = array();
$admins = get_users(array('role' => 'administrator', 'number' => 1, 'fields' => 'ID'));
if ($admins) wp_set_current_user((int) $admins[0]);
require_once ABSPATH . 'wp-admin/includes/file.php';
require_once ABSPATH . 'wp-admin/includes/media.php';
require_once ABSPATH . 'wp-admin/includes/image.php';
add_filter('upload_mimes', function ($m) { $m['svg'] = 'image/svg+xml'; return $m; });
add_filter('wp_check_filetype_and_ext', function ($d, $file, $filename) {
	if (substr($filename, -4) === '.svg') { $d['ext'] = 'svg'; $d['type'] = 'image/svg+xml'; $d['proper_filename'] = $filename; }
	return $d;
}, 10, 3);

$media = get_option('pv_media_map', array());
function pv_import($key, $url, $filename, $alt, &$media) {
	if (!empty($media[$key]) && is_int($media[$key]) && get_post($media[$key])) return;
	$tmp = download_url($url, 90);
	if (is_wp_error($tmp)) { $media[$key] = 'ERR ' . $tmp->get_error_message(); return; }
	$id = media_handle_sideload(array('name' => $filename, 'tmp_name' => $tmp), 0, $alt);
	if (is_wp_error($id)) { $media[$key] = 'ERR ' . $id->get_error_message(); return; }
	update_post_meta($id, '_wp_attachment_image_alt', $alt);
	$media[$key] = $id;
}

$icons = array('house', 'pen', 'pipe', 'check', 'doc', 'factory', 'tower', 'network', 'alert', 'arrow-ur', 'download', 'mail2');
foreach ($icons as $i) {
	pv_import('pv-icon-' . $i, PV_SRC . 'wp-content/themes/pyhtaa-child/assets/svg/pv-icon-' . $i . '.svg', 'pv-icon-' . $i . '.svg', '', $media);
}
$px = function ($id, $w = 1600) { return "https://images.pexels.com/photos/$id/pexels-photo-$id.jpeg?auto=compress&cs=tinysrgb&w=$w"; };
$photos = array(
	'pl-hero'        => array($px(14953886), 'Vesijohtoasennus'),
	'pl-pvok'        => array($px(6419128), 'Vesiosuuskunnan laitteiden huolto'),
	'pl-shareholder' => array($px(2893177), 'Kiinteistön vesilaitteet'),
	'ct-hero'        => array($px(30624054), 'Pyhtään maisemaa'),
	'pm-hero'        => array($px(17335757), 'Kiinteistöpumppaamo'),
	'pm-wash'        => array($px(17335758, 1200), 'Pumppaamon pesu'),
	'wi-hero'        => array($px(416528), 'Raikasta vettä'),
	'wi-reduce'      => array($px(6857798), 'Vedenkulutuksen vähentäminen kotona'),
	'sh-hero'        => array($px(6963888), 'Osakkaiden kokous'),
	'sh-meetings'    => array($px(6964363, 1200), 'Kokous'),
	'sh-agreements'  => array($px(10432372, 1200), 'Sopimuksen allekirjoitus'),
	'sh-reports'     => array($px(5900074, 2000), 'Vuosiraportit'),
	'wq-hero'        => array($px(954585), 'Vesinäyte laboratoriossa'),
);
foreach ($photos as $k => $p) pv_import($k, $p[0], 'pv-' . $k . '.jpg', $p[1], $media);
pv_import('pm-nature', PV_SRC . 'wp-content/themes/pyhtaa-child/assets/img/pv-ducks-litter.jpg', 'pv-pm-nature.jpg',
	'Sorsat rannalla roskien keskellä', $media);

update_option('pv_media_map', $media, false);
foreach ($media as $k => $v) $out[$k] = is_int($v) ? array($v, wp_get_attachment_url($v)) : $v;
echo wp_json_encode($out);
