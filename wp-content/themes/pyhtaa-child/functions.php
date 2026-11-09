<?php
/**
 * Pyhtää Vesiosuuskunta – Hello Elementor child theme.
 *
 * @package pyhtaa-child
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

define( 'PYHTAA_CHILD_VERSION', '1.0.0' );

/**
 * Parent + child styles, then the design behaviours (animations, drawer, reveal).
 */
add_action( 'wp_enqueue_scripts', function () {
	$dir = get_stylesheet_directory();
	$uri = get_stylesheet_directory_uri();

	wp_enqueue_style( 'hello-elementor-child', get_stylesheet_uri(), array(),PYHTAA_CHILD_VERSION );
	wp_enqueue_style( 'pyhtaa-site', $uri . '/assets/pv-site.css', array(), filemtime( $dir . '/assets/pv-site.css' ) );
	wp_enqueue_script( 'pyhtaa-site', $uri . '/assets/pv-site.js', array(), filemtime( $dir . '/assets/pv-site.js' ), array( 'in_footer' => true, 'strategy' => 'defer' ) );
}, 20 );

/**
 * Let administrators upload SVG files (logo, icons and decorative waves are SVG).
 */
add_filter( 'upload_mimes', function ( $mimes ) {
	if ( current_user_can( 'manage_options' ) ) {
		$mimes['svg'] = 'image/svg+xml';
	}
	return $mimes;
} );

/**
 * Finnish wording for the few Ultimate Addons for Elementor (header-footer-elementor)
 * front-end strings that have no Finnish translation pack.
 */
add_filter( 'gettext_header-footer-elementor', function ( $translation, $text ) {
	$fi = array(
		'Skip to main content' => 'Siirry pääsisältöön',
		'Menu'                 => 'Valikko',
		'Menu Toggle'          => 'Avaa valikko',
		'Close'                => 'Sulje',
	);
	return isset( $fi[ $text ] ) ? $fi[ $text ] : $translation;
}, 10, 2 );
