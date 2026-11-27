<?php
/**
 * Setup step 5 – inner pages (run with the same WP-CLI loader as the other steps).
 * Refreshes the child theme CSS/JS and saves the 7 inner pages from tools/data/page-<slug>.json
 * as Elementor documents (Elementor Full Width template, page title hidden).
 * The board page ("Hallitus") is password protected; PV_BOARD_PW sets its password once.
 */
if (!defined('PV_SRC')) exit('PV_SRC not defined');
$out = array();
$admins = get_users(array('role' => 'administrator', 'number' => 1, 'fields' => 'ID'));
if ($admins) wp_set_current_user((int) $admins[0]);

function pv_fetch5($rel) {
	$r = wp_remote_get(PV_SRC . $rel, array('timeout' => 30));
	if (is_wp_error($r) || wp_remote_retrieve_response_code($r) !== 200) throw new Exception('fetch failed: ' . $rel);
	return wp_remote_retrieve_body($r);
}

$dir = get_theme_root() . '/pyhtaa-child';
foreach (array('assets/pv-site.css', 'assets/pv-site.js') as $rel) {
	file_put_contents($dir . '/' . $rel, pv_fetch5('wp-content/themes/pyhtaa-child/' . $rel));
}

$map = array(
	'hinnasto' => 'Price list', 'yhteystiedot' => 'Contact', 'hallitus' => 'Board pages',
	'pumppaamon-huolto' => 'Pumping station maintenance', 'yleista-tietoa-vedesta' => 'General water information',
	'osakkaat' => 'Members', 'vedenlaatutulokset' => 'Water quality results',
);
$pages = get_option('pv_page_map');
foreach ($map as $slug => $key) {
	$id = (int) $pages[$key];
	$elements = json_decode(pv_fetch5('tools/data/page-' . $slug . '.json'), true);
	update_post_meta($id, '_wp_page_template', 'elementor_header_footer');
	update_post_meta($id, '_elementor_edit_mode', 'builder');
	$doc = \Elementor\Plugin::$instance->documents->get($id, false);
	$doc->save(array('elements' => $elements, 'settings' => array('template' => 'elementor_header_footer', 'hide_title' => 'yes')));
	$out[$slug] = array($id, get_permalink($id), strlen(get_post_meta($id, '_elementor_data', true)));
}

/* board page: password protection (set once; later changes are made in the page settings) */
$board = (int) $pages['Board pages'];
if (defined('PV_BOARD_PW') && get_post_field('post_password', $board) === '') {
	wp_update_post(array('ID' => $board, 'post_password' => PV_BOARD_PW));
}
$out['board_protected'] = get_post_field('post_password', $board) !== '';

/* documents live in this site's Media Library: re-point links from the old site (see setup-8-relink.php) */
if (get_option('pv_doc_map')) {
	$rl = wp_remote_get(PV_SRC . 'tools/setup-8-relink.php', array('timeout' => 30));
	if (wp_remote_retrieve_response_code($rl) === 200) { ob_start(); eval('?>' . wp_remote_retrieve_body($rl)); $out['relink'] = json_decode(ob_get_clean(), true); }
}

\Elementor\Plugin::$instance->files_manager->clear_cache();
wp_cache_flush();
echo wp_json_encode($out);
