<?php
/**
 * Setup step 11 – Main Menu: inner-page items back to "#" placeholders (as requested); Etusivu keeps linking to Home.
 * Each Page item becomes a Custom Link "#" with the same label, order and CSS classes.
 * To link them to the real pages again, run setup-10-menu.php.
 */
if (!defined('PV_SRC')) exit('PV_SRC not defined');
$admins = get_users(array('role' => 'administrator', 'number' => 1, 'fields' => 'ID'));
if ($admins) wp_set_current_user((int) $admins[0]);

$home = (int) get_option('page_on_front');
$menu_id = 2;
foreach (wp_get_nav_menu_items($menu_id) as $item) {
	if ($item->type !== 'post_type' || $item->object !== 'page' || (int) $item->object_id === $home) continue;
	wp_update_nav_menu_item($menu_id, $item->ID, array(
		'menu-item-type'      => 'custom',
		'menu-item-object'    => 'custom',
		'menu-item-object-id' => 0,
		'menu-item-url'       => '#',
		'menu-item-title'     => $item->title,
		'menu-item-position'  => $item->menu_order,
		'menu-item-parent-id' => $item->menu_item_parent,
		'menu-item-classes'   => implode(' ', array_filter((array) $item->classes)),
		'menu-item-status'    => 'publish',
	));
}
$out = array();
foreach (wp_get_nav_menu_items($menu_id) as $item) $out[] = array($item->menu_order, $item->title, $item->url);
wp_cache_flush();
echo wp_json_encode($out);
