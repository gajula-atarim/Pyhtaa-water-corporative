<?php
/**
 * Setup step 10 – link the Main Menu items to the real pages (they were "#" placeholders).
 * Each custom "#" item becomes a normal Page item (WP Admin → Appearance → Menus), keeping its label,
 * order and CSS classes. Page items follow the page if its address changes later.
 */
if (!defined('PV_SRC')) exit('PV_SRC not defined');
$admins = get_users(array('role' => 'administrator', 'number' => 1, 'fields' => 'ID'));
if ($admins) wp_set_current_user((int) $admins[0]);

$pages = get_option('pv_page_map');
$by_label = array(
	'Vedenlaatutulokset'     => 'Water quality results',
	'Hinnasto'               => 'Price list',
	'Yleistä tietoa vedestä' => 'General water information',
	'Osakkaat'               => 'Members',
	'Hallitus'               => 'Board pages',
	'Yhteystiedot'           => 'Contact',
	'Pumppaamon huolto'      => 'Pumping station maintenance',
);
$menu_id = 2;
$out = array();
foreach (wp_get_nav_menu_items($menu_id) as $item) {
	if ($item->type !== 'custom' || !isset($by_label[$item->title])) continue;
	$page_id = (int) $pages[$by_label[$item->title]];
	wp_update_nav_menu_item($menu_id, $item->ID, array(
		'menu-item-object-id' => $page_id,
		'menu-item-object'    => 'page',
		'menu-item-type'      => 'post_type',
		'menu-item-title'     => $item->title,
		'menu-item-position'  => $item->menu_order,
		'menu-item-parent-id' => $item->menu_item_parent,
		'menu-item-classes'   => implode(' ', array_filter((array) $item->classes)),
		'menu-item-status'    => 'publish',
	));
}
foreach (wp_get_nav_menu_items($menu_id) as $item) $out[] = array($item->menu_order, $item->title, $item->url);
wp_cache_flush();
echo wp_json_encode($out);
