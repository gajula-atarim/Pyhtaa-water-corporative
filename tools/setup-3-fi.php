<?php
/**
 * Setup step 3 – Finnish content (run with the same WP-CLI loader as the other steps).
 * Site language fi (front end), admins keep an English dashboard, Finnish site title,
 * page titles/slugs, menu labels and image alt texts.
 */
if (!defined('PV_SRC')) exit('PV_SRC not defined');
$out = array();

/* 1. language packs: core + plugins + themes, then make Finnish the site language */
foreach (array('language core install fi', 'language plugin install --all fi', 'language theme install --all fi') as $cmd) {
	$r = WP_CLI::runcommand($cmd, array('return' => 'all', 'exit_error' => false, 'launch' => false));
	$out['cli'][] = $cmd . ' => ' . trim(substr(($r->stdout ?: '') . ($r->stderr ?: ''), 0, 160));
}
$avail = get_available_languages();
if (in_array('fi', $avail, true)) update_option('WPLANG', 'fi');
$out['WPLANG'] = get_option('WPLANG');
foreach (get_users(array('role' => 'administrator', 'fields' => 'ID')) as $uid) {
	if (!get_user_meta($uid, 'locale', true)) update_user_meta($uid, 'locale', 'en_US'); // dashboard stays English
}

/* 2. site title */
update_option('blogname', 'Pyhtään vesiosuuskunta');

/* 3. pages: Finnish titles + slugs */
$fi = array(
	'Home' => array('Etusivu', 'etusivu'),
	'Water quality results' => array('Vedenlaatutulokset', 'vedenlaatutulokset'),
	'Price list' => array('Hinnasto', 'hinnasto'),
	'Meter readings' => array('Mittarilukemat', 'mittarilukemat'),
	'General water information' => array('Yleistä tietoa vedestä', 'yleista-tietoa-vedesta'),
	'Members' => array('Osakkaat', 'osakkaat'),
	'Board pages' => array('Hallitus', 'hallitus'),
	'Contact' => array('Yhteystiedot', 'yhteystiedot'),
	'Pumping station maintenance' => array('Pumppaamon huolto', 'pumppaamon-huolto'),
);
$pages = get_option('pv_page_map');
foreach ($fi as $en => $t) {
	if (empty($pages[$en])) continue;
	wp_update_post(array('ID' => (int) $pages[$en], 'post_title' => $t[0], 'post_name' => $t[1]));
	$out['pages'][$t[0]] = get_permalink((int) $pages[$en]);
}

/* 4. menu labels (custom '#' items keep their own title) */
$labels = array();
foreach ($fi as $en => $t) $labels[$en] = $t[0];
foreach (wp_get_nav_menu_items(2) as $it) {
	if ($it->type !== 'custom') continue;
	$title = get_post_field('post_title', $it->ID);
	if (isset($labels[$title])) {
		wp_update_post(array('ID' => $it->ID, 'post_title' => $labels[$title]));
		$out['menu'][] = $labels[$title];
	}
}

/* 5. Finnish alt texts for the photos */
$alts = array(
	'hero-lake' => 'Järvimaisema ja punainen aitta Pyhtäällä',
	'hero-tap' => 'Lasiin valuu raikasta hanavettä',
	'water-meter' => 'Lähikuva vesimittarista',
	'member-home' => 'Osakas laskee hanavettä lasiin kotonaan',
	'billing' => 'Pariskunta käy läpi laskujaan kotona',
	'cabin-lake' => 'Mökki järven rannalla Suomessa',
);
$media = get_option('pv_media_map');
foreach ($alts as $k => $alt) {
	if (!empty($media[$k]) && is_int($media[$k])) {
		update_post_meta($media[$k], '_wp_attachment_image_alt', $alt);
		wp_update_post(array('ID' => $media[$k], 'post_title' => $alt));
	}
}

\Elementor\Plugin::$instance->files_manager->clear_cache();
wp_cache_flush();
echo wp_json_encode($out);
