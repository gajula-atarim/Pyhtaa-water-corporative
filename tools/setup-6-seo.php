<?php
/**
 * Setup step 6 – Yoast SEO titles and meta descriptions (run with the same WP-CLI loader as the other steps).
 * Reads tools/data/seo.json ({page ID: {title, desc}}), stores them as Yoast's per-page fields
 * (editable later in the Yoast box of each page) and refreshes Yoast's indexables for those pages.
 */
if (!defined('PV_SRC')) exit('PV_SRC not defined');
$admins = get_users(array('role' => 'administrator', 'number' => 1, 'fields' => 'ID'));
if ($admins) wp_set_current_user((int) $admins[0]);

$r = wp_remote_get(PV_SRC . 'tools/data/seo.json', array('timeout' => 30));
if (wp_remote_retrieve_response_code($r) !== 200) exit('fetch failed');
$seo = json_decode(wp_remote_retrieve_body($r), true);
$out = array();
foreach ($seo as $id => $m) {
	$id = (int) $id;
	update_post_meta($id, '_yoast_wpseo_title', wp_slash($m['title']));
	update_post_meta($id, '_yoast_wpseo_metadesc', wp_slash($m['desc']));
	clean_post_cache($id);
	// rebuild Yoast's cached copy of the page so the new values show on the front end straight away
	try {
		if (function_exists('YoastSEO')) {
			$repo = YoastSEO()->classes->get(\Yoast\WP\SEO\Repositories\Indexable_Repository::class);
			$builder = YoastSEO()->classes->get(\Yoast\WP\SEO\Builders\Indexable_Builder::class);
			$idx = $repo->find_by_id_and_type($id, 'post', false);
			$builder->build_for_id_and_type($id, 'post', $idx ?: false);
		}
	} catch (Throwable $e) { $out['indexable_error_' . $id] = $e->getMessage(); }
	$out[$id] = array(get_post_meta($id, '_yoast_wpseo_title', true), get_post_meta($id, '_yoast_wpseo_metadesc', true));
}
echo wp_json_encode($out);
