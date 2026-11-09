<?php
/**
 * Setup step 2 – run on the site with WP-CLI (same loader as setup-1.php).
 * Refreshes the child theme files, sets the Elementor kit globals and saves the
 * header/footer (Ultimate Addons for Elementor templates) and the Home page from tools/data/*.json.
 */
if (!defined('PV_SRC')) exit('PV_SRC not defined');
$out = array();
$admins = get_users(array('role'=>'administrator','number'=>1,'fields'=>'ID'));
if ($admins) wp_set_current_user((int)$admins[0]);

function pv_fetch($rel) {
	$r = wp_remote_get(PV_SRC . $rel, array('timeout' => 30));
	if (is_wp_error($r) || wp_remote_retrieve_response_code($r) !== 200) throw new Exception('fetch failed: ' . $rel);
	return wp_remote_retrieve_body($r);
}

/* 1. theme files (refresh) */
$dir = get_theme_root() . '/pyhtaa-child';
foreach (array('style.css','functions.php','assets/pv-site.css','assets/pv-site.js') as $rel) {
	file_put_contents($dir . '/' . $rel, pv_fetch('wp-content/themes/pyhtaa-child/' . $rel));
}

/* 2. kit globals */
$kit = \Elementor\Plugin::$instance->kits_manager->get_active_kit();
$ks = $kit->get_settings();
$sys = array(array('_id'=>'primary','title'=>'Water Blue','color'=>'#1F5F99'), array('_id'=>'secondary','title'=>'Deep Navy','color'=>'#0B2E4F'),
	array('_id'=>'text','title'=>'Body Text','color'=>'#3A4854'), array('_id'=>'accent','title'=>'Sun Yellow','color'=>'#F2B53A'));
$custom = array();
foreach (array('pvsky'=>array('Sky','#5FA8D3'),'pvcream'=>array('Cream Background','#F7F6F2'),'pvink'=>array('Ink','#14202B'),'pvgrey'=>array('Slate Grey','#4A5966'),
	'pvmist'=>array('Mist','#E8F1F7'),'pvice'=>array('Ice','#D6E8F4'),'pvpale'=>array('Pale Blue','#A9D1EA'),'pvline'=>array('Line Grey','#C9D6E0'),
	'pvwhite'=>array('White','#FFFFFF'),'pvdeep'=>array('Footer Deep Navy','#082440')) as $id=>$c) $custom[] = array('_id'=>$id,'title'=>$c[0],'color'=>$c[1]);
$ft = function($id,$title,$w){ return array('_id'=>$id,'title'=>$title,'typography_typography'=>'custom','typography_font_family'=>'Poppins','typography_font_weight'=>$w); };
$ks = array_merge($ks, array(
	'system_colors' => $sys, 'custom_colors' => $custom,
	'system_typography' => array($ft('primary','Headings','600'), $ft('secondary','Secondary','500'), $ft('text','Body','400'), $ft('accent','Buttons','600')),
	'body_background_background' => 'classic', 'body_background_color' => '#F7F6F2',
	'body_color' => '#14202B',
	'body_typography_typography' => 'custom', 'body_typography_font_family' => 'Poppins',
	'body_typography_font_size' => array('unit'=>'px','size'=>16,'sizes'=>array()), 'body_typography_line_height' => array('unit'=>'em','size'=>1.5,'sizes'=>array()),
	'link_normal_color' => '#1F5F99', 'link_hover_color' => '#0B2E4F',
	'container_width' => array('unit'=>'px','size'=>1200,'sizes'=>array()),
	'container_padding' => array('unit'=>'px','top'=>'0','right'=>'0','bottom'=>'0','left'=>'0','isLinked'=>true),
	'space_between_widgets' => array('unit'=>'px','column'=>'0','row'=>'0','isLinked'=>true,'size'=>0),
	'site_name' => 'Pyhtään vesiosuuskunta',
));
$kit->save(array('settings' => $ks));
$out['kit'] = $kit->get_id();

/* 3. documents */
function pv_save_doc($post_id, $elements, $settings = array()) {
	$doc = \Elementor\Plugin::$instance->documents->get($post_id, false);
	if (!$doc) throw new Exception('no document for ' . $post_id);
	update_post_meta($post_id, '_elementor_edit_mode', 'builder');
	$doc->save(array('elements' => $elements, 'settings' => $settings));
	return $doc->get_main_id();
}
$pages = get_option('pv_page_map');
$home = (int) $pages['Home'];
update_post_meta($home, '_wp_page_template', 'elementor_header_footer');
pv_save_doc($home, json_decode(pv_fetch('tools/data/home.json'), true), array('template' => 'elementor_header_footer', 'hide_title' => 'yes'));
$out['home'] = array($home, get_permalink($home), strlen(get_post_meta($home, '_elementor_data', true)));

$hf = get_option('pv_hf_map', array());
foreach (array('header' => array('Site Header', 'type_header'), 'footer' => array('Site Footer', 'type_footer')) as $k => $info) {
	if (empty($hf[$k]) || !get_post($hf[$k])) {
		$hf[$k] = wp_insert_post(array('post_type' => 'elementor-hf', 'post_status' => 'publish', 'post_title' => $info[0]));
	}
	$id = (int) $hf[$k];
	update_post_meta($id, 'ehf_template_type', $info[1]);
	update_post_meta($id, 'ehf_target_include_locations', array('rule' => array('basic-global'), 'specific' => array()));
	update_post_meta($id, 'ehf_target_exclude_locations', array());
	update_post_meta($id, 'ehf_target_user_roles', array('all'));
	update_post_meta($id, '_wp_page_template', 'elementor_canvas');
	pv_save_doc($id, json_decode(pv_fetch('tools/data/' . $k . '.json'), true));
	$out[$k] = array($id, strlen(get_post_meta($id, '_elementor_data', true)));
}
update_option('pv_hf_map', $hf, false);

/* 4. caches */
\Elementor\Plugin::$instance->files_manager->clear_cache();
$out['hfe_header'] = function_exists('get_hfe_header_id') ? get_hfe_header_id() : 'n/a';
$out['hfe_footer'] = function_exists('get_hfe_footer_id') ? get_hfe_footer_id() : 'n/a';
echo wp_json_encode($out);
