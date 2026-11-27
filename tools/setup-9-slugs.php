<?php
/**
 * Setup step 9 – give four pages the same addresses (slugs) they have on the old site pyhtaanvok.fi,
 * so Google results, bookmarks and old links keep working after launch.
 * (The interim addresses used during the build were never public, so they need no redirect.)
 */
if (!defined('PV_SRC')) exit('PV_SRC not defined');
$admins = get_users(array('role' => 'administrator', 'number' => 1, 'fields' => 'ID'));
if ($admins) wp_set_current_user((int) $admins[0]);

$pages = get_option('pv_page_map');
$slugs = array(
	'Water quality results'       => 'toiminta',
	'General water information'   => 'vesitietoa',
	'Pumping station maintenance' => 'pumppaamoiden-huolto-ohjeita',
	'Board pages'                 => 'hallituksen-sivut',
);
$out = array();
foreach ($slugs as $key => $slug) {
	$id = (int) $pages[$key];
	$taken = get_page_by_path($slug, OBJECT, array('page', 'post'));
	if ($taken && (int) $taken->ID !== $id) { $out[$key] = 'slug already used by #' . $taken->ID; continue; }
	if (get_post_field('post_name', $id) !== $slug) {
		wp_update_post(array('ID' => $id, 'post_name' => $slug)); // keeps password, content and Elementor data
	}
	$out[$key] = array($id, get_permalink($id));
}
flush_rewrite_rules(false);
\Elementor\Plugin::$instance->files_manager->clear_cache();
wp_cache_flush();
echo wp_json_encode($out);
