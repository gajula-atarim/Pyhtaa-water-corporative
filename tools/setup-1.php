<?php
/**
 * Setup step 1 – run on the site with WP-CLI:
 *   wp eval "define('PV_SRC','<raw repo base>/'); eval('?>'.wp_remote_retrieve_body(wp_remote_get(PV_SRC.'tools/setup-1.php')));"
 * Installs the child theme files from this repository, imports media, creates pages + menu,
 * sets Elementor options and prints the widget control keys used by the page builder script.
 */
if (!defined('PV_SRC')) exit('PV_SRC not defined');
$out = array();
$files = array('style.css','functions.php','assets/pv-site.css','assets/pv-site.js');
$svgs = array('pv-edge-cream-6','pv-edge-cream-8','pv-edge-cream-m4','pv-edge-mist-4','pv-edge-navy-0','pv-edge-navy-m6','pv-edge-yellow-0','pv-icon-arrow-up','pv-icon-drop','pv-icon-euro','pv-icon-mail','pv-icon-meter','pv-icon-phone','pv-icon-phone-line','pv-icon-phone-solid','pv-icon-pin','pv-lines-blue','pv-lines-navy','pv-lines-sky','pv-lines-yellow','pv-logo-drop','pv-logo-drop-footer','pv-sun-drop');
foreach ($svgs as $s) $files[] = 'assets/svg/' . $s . '.svg';
$admins = get_users(array('role'=>'administrator','number'=>1,'fields'=>'ID'));
if ($admins) wp_set_current_user((int)$admins[0]);
$out['user'] = get_current_user_id();
/* 1. child theme */
$dir = get_theme_root() . '/pyhtaa-child';
foreach ($files as $rel) { $r = wp_remote_get(PV_SRC . 'wp-content/themes/pyhtaa-child/' . $rel, array('timeout'=>30)); if (is_wp_error($r) || wp_remote_retrieve_response_code($r) !== 200) { $out['fetch_errors'][] = $rel; continue; } $p = $dir . '/' . $rel; wp_mkdir_p(dirname($p)); file_put_contents($p, wp_remote_retrieve_body($r)); }
$out['theme_files'] = count($files);
switch_theme('pyhtaa-child');
$out['active_theme'] = get_stylesheet() . ' / parent ' . get_template();
/* 2. media */
require_once ABSPATH . 'wp-admin/includes/file.php'; require_once ABSPATH . 'wp-admin/includes/media.php'; require_once ABSPATH . 'wp-admin/includes/image.php';
add_filter('upload_mimes', function($m){ $m['svg']='image/svg+xml'; return $m; });
add_filter('wp_check_filetype_and_ext', function($d,$file,$filename){ if (substr($filename,-4)==='.svg') { $d['ext']='svg'; $d['type']='image/svg+xml'; $d['proper_filename']=$filename; } return $d; }, 10, 3);
$media = get_option('pv_media_map', array());
foreach (glob($dir . '/assets/svg/*.svg') as $svg) {
  $name = basename($svg, '.svg'); if (!empty($media[$name]) && get_post($media[$name])) continue;
  $tmp = wp_tempnam($name . '.svg'); copy($svg, $tmp);
  $id = media_handle_sideload(array('name'=>$name . '.svg','tmp_name'=>$tmp), 0, $name);
  $media[$name] = is_wp_error($id) ? $id->get_error_message() : $id;
}
$photos = array(
 'hero-lake'=>array('https://images.pexels.com/photos/3109271/pexels-photo-3109271.jpeg?auto=compress&cs=tinysrgb&w=1600','Lake in Pyhtää area (photo: Olivier Darny / Pexels)'),
 'hero-tap'=>array('https://images.pexels.com/photos/12644991/pexels-photo-12644991.jpeg?auto=compress&cs=tinysrgb&w=1200','Glass of tap water (photo: BOOM Photography / Pexels)'),
 'water-meter'=>array('https://images.pexels.com/photos/4494653/pexels-photo-4494653.jpeg?auto=compress&cs=tinysrgb&w=1200','Close-up of a water meter (photo: Nothing Ahead / Pexels)'),
 'member-home'=>array('https://images.pexels.com/photos/33768875/pexels-photo-33768875.jpeg?auto=compress&cs=tinysrgb&w=1600','Filling a glass with tap water at home (photo: Centre for Ageing Better / Pexels)'),
 'billing'=>array('https://images.pexels.com/photos/6964105/pexels-photo-6964105.jpeg?auto=compress&cs=tinysrgb&w=1600','Couple looking at their bills (photo: Mikhail Nilov / Pexels)'),
 'cabin-lake'=>array('https://images.pexels.com/photos/27869122/pexels-photo-27869122.jpeg?auto=compress&cs=tinysrgb&w=1600','Cabin near a lake in Finland (photo: Jon Eliya / Pexels)'),
);
foreach ($photos as $name => $p) {
  if (!empty($media[$name]) && is_int($media[$name]) && get_post($media[$name])) continue;
  $tmp = download_url($p[0], 60);
  if (is_wp_error($tmp)) { $media[$name] = 'ERR ' . $tmp->get_error_message(); continue; }
  $id = media_handle_sideload(array('name'=>'pv-' . $name . '.jpg','tmp_name'=>$tmp), 0, $p[1]);
  if (!is_wp_error($id)) update_post_meta($id, '_wp_attachment_image_alt', $p[1]);
  $media[$name] = is_wp_error($id) ? 'ERR ' . $id->get_error_message() : $id;
}
update_option('pv_media_map', $media, false);
$out['media'] = array(); foreach ($media as $k=>$v) $out['media'][$k] = is_int($v) ? array($v, wp_get_attachment_url($v)) : $v;
/* 3. pages + menu */
$titles = array('Home','Water quality results','Price list','Meter readings','General water information','Members','Board pages','Contact','Pumping station maintenance');
$pages = get_option('pv_page_map', array());
foreach ($titles as $t) {
  if (!empty($pages[$t]) && get_post($pages[$t])) continue;
  $pages[$t] = wp_insert_post(array('post_type'=>'page','post_status'=>'publish','post_title'=>$t,'post_name'=>sanitize_title($t),'post_content'=>''));
}
update_option('pv_page_map', $pages, false);
update_option('show_on_front','page'); update_option('page_on_front', $pages['Home']);
$menu = wp_get_nav_menu_object('Main Menu');
$menu_id = $menu ? $menu->term_id : wp_create_nav_menu('Main Menu');
if (!wp_get_nav_menu_items($menu_id)) { foreach ($titles as $i => $t) wp_update_nav_menu_item($menu_id, 0, array('menu-item-title'=>$t,'menu-item-object'=>'page','menu-item-object-id'=>$pages[$t],'menu-item-type'=>'post_type','menu-item-status'=>'publish','menu-item-position'=>$i+1)); }
$out['pages'] = array(); foreach ($pages as $t=>$id) $out['pages'][$t] = array($id, get_permalink($id));
$out['menu'] = array($menu_id, get_term($menu_id)->slug);
/* 4. Elementor settings */
update_option('elementor_disable_color_schemes','yes'); update_option('elementor_disable_typography_schemes','yes');
update_option('elementor_unfiltered_files_upload','1'); update_option('elementor_font_display','swap');
$cpt = (array) get_option('elementor_cpt_support', array('page','post')); foreach (array('page','post') as $c) if (!in_array($c,$cpt)) $cpt[]=$c; update_option('elementor_cpt_support',$cpt);
$out['elementor_version'] = defined('ELEMENTOR_VERSION') ? ELEMENTOR_VERSION : null;
$out['hfe_version'] = defined('HFE_VER') ? HFE_VER : null;
$out['kit'] = get_option('elementor_active_kit');
$out['experiments'] = array();
if (class_exists('\Elementor\Plugin')) { $em = \Elementor\Plugin::$instance->experiments; foreach (array('container','nested-elements','e_atomic_elements','e_optimized_markup','e_font_icon_svg') as $f) $out['experiments'][$f] = $em->is_feature_active($f); }
/* 5. control introspection */
function pv_ctrls($controls, $filter=null) { $r=array(); foreach ($controls as $k=>$c) { if ($filter && !preg_match($filter,$k)) continue; if (in_array($c['type'],array('section','tab','tabs','heading','divider','raw_html','popover_toggle_end'))) continue; $e=$c['type']; if (!empty($c['size_units'])) $e.=' ['.implode(',',$c['size_units']).']'; if (!empty($c['options']) && is_array($c['options']) && count($c['options'])<12) $e.=' {'.implode('|',array_map('strval',array_keys($c['options']))).'}'; if (isset($c['default']) && !is_array($c['default']) && $c['default']!=='') $e.=' ='.$c['default']; $r[$k]=$e; } return $r; }
$el = \Elementor\Plugin::$instance->elements_manager->get_element_types('container');
$out['ctrl_container'] = $el ? pv_ctrls($el->get_controls(), '/^(content_width|boxed_width|width|min_height|flex_|_flex|gap|html_tag|link|padding|margin|position|_position|_offset|z_index|overflow|css_classes|_element_id|border_|box_shadow_box_shadow_type|background_(background|color|image|size|position|repeat)$|background_overlay_(background|color|color_b|color_stop|color_b_stop|gradient_angle|gradient_type)$|grid_|container_type)/') : 'none';
$wm = \Elementor\Plugin::$instance->widgets_manager;
foreach (array('navigation-menu','copyright','site-logo','hfe-site-logo','retina','site-title') as $w) { $t=$wm->get_widget_types($w); if ($t) $out['ctrl_'.$w] = pv_ctrls($t->get_controls(), '/^(?!_)/'); }
$out['hfe_widgets'] = array_values(array_filter(array_keys($wm->get_widget_types()), function($k){ return strpos($k,'hfe')!==false || in_array($k,array('navigation-menu','copyright','site-logo','retina','site-title','page-title','post-info','search-button','cart','site-tagline','breadcrumbs-widget','scroll-to-top','infocard','basic-posts')); }));
$out['ctrl_button'] = pv_ctrls($wm->get_widget_types('button')->get_controls(), '/^(?!_)/');
$out['ctrl_common'] = pv_ctrls($wm->get_widget_types('heading')->get_controls(), '/^_(element_width|element_custom_width|flex|position|offset|z_index|css_classes|background_background|background_color|border_radius|padding|margin)/');
$out['ctrl_heading'] = pv_ctrls($wm->get_widget_types('heading')->get_controls(), '/^(?!_)/');
$out['ctrl_icon'] = pv_ctrls($wm->get_widget_types('icon')->get_controls(), '/^(?!_)/');
$out['ctrl_icon_list'] = pv_ctrls($wm->get_widget_types('icon-list')->get_controls(), '/^(?!_)/');
$out['ctrl_text'] = pv_ctrls($wm->get_widget_types('text-editor')->get_controls(), '/^(?!_)/');
$out['ctrl_image'] = pv_ctrls($wm->get_widget_types('image')->get_controls(), '/^(?!_)/');
echo wp_json_encode($out);
