import { ItemData } from './hmaxData';

type ImageRule = {
  terms: string[];
  path: string;
};

// Only map an image when its filename/model identity matches the dump record.
// Records without a matching source image remain image-less and are reported in the UI.
const DUMP_IMAGE_RULES: ImageRule[] = [
  { terms: ['honor 50 lite'], path: '/images/honor_50_lite_ntn_l22_c185_new.jpg' },
  { terms: ['fne nx9'], path: '/images/honor_70_fne-nx9_official_hmax.jpg' },
  { terms: ['x7a', 'rky lx2'], path: '/images/honor_x7a_rky_lx2_2gb_dump_f64.jpg' },
  { terms: ['x9c'], path: '/images/honor_x9c_full_dump.jpg' },
  { terms: ['honor 400'], path: '/images/honor_400_abr_n03_osv15_full_dump_f64_ultra.jpg' },
  { terms: ['x7b 5g'], path: '/images/honor_x7b_5g_clk_nx2_frp_ymtc_hmax.jpg' },
  { terms: ['x7b', 'clk lx2'], path: '/images/honor_x7b_clk_lx2_c185.jpg' },
  { terms: ['huawei y7a'], path: '/images/huawei_y7a_ppa_lx2.jpg' },
  { terms: ['ppa lx2'], path: '/images/huawei_y7a_ppa_lx2.jpg' },
  { terms: ['hmd aura'], path: '/images/hmd_aura_ta1631_hmax_final.jpg' },
  { terms: ['ta 1631'], path: '/images/hmd_aura_ta1631_hmax_final.jpg' },
  { terms: ['benco v60'], path: '/images/benco_v60_full_dump_cm2.jpg' },
  { terms: ['benco s1 pro'], path: '/images/benco_s1_pro_ae9260_dual_dump.jpg' },
  { terms: ['kxd a07'], path: '/images/kxd_a07_dual_hmax.jpg' },
  { terms: ['nokia c12'], path: '/images/nokia_c12_ta1583_pandora_hmax.jpg' },
  { terms: ['ta 1583'], path: '/images/nokia_c12_ta1583_pandora_hmax.jpg' },
  { terms: ['nokia c10'], path: '/images/nokia_c10_ta_1342_sc7731e.jpg' },
  { terms: ['ta 1342'], path: '/images/nokia_c10_ta_1342_sc7731e.jpg' },
  { terms: ['nokia 5 3'], path: '/images/nokia_5_3_ta_1234_00ww_2_290_sp02.jpg' },
  { terms: ['ta 1234'], path: '/images/nokia_5_3_ta_1234_00ww_2_290_sp02.jpg' },
  { terms: ['ta 1114'], path: '/images/nokia_ta_1114_copy_spreadtrum_miracle.jpg' },
  { terms: ['ta 1380'], path: '/images/ta1380_hmax.jpg' },
  { terms: ['nokia c22'], path: '/images/nokia_c22_ta1539_00ww_1_520_hmax.jpg' },
  { terms: ['smart 6', 'x6511b'], path: '/images/infinix_smart6_x6511b_factory_hmax.jpg' },
  { terms: ['smart 20', 'x6840b'], path: '/images/infinix_smart20_x6840b_dump_hmax.jpg' },
  { terms: ['note 30 5g'], path: '/images/infinix_note_30_5g_x6711_v600.jpg' },
  { terms: ['smart 5', 'x657c'], path: '/images/infinix_smart5_x657c_full_nv_dump.jpg' },
  { terms: ['itel p37'], path: '/images/itel_p37_p651w.jpg' },
  { terms: ['itel a06'], path: '/images/itel_a06_a669w_full_dump_v1604_unlocktool_hamallah.jpg' },
  { terms: ['a49', 'a661l'], path: '/images/itel_a49_a661l_a58pro_pandora_hmax.jpg' },
  { terms: ['s23', 's665ln'], path: '/images/itel_s23_s665ln_f065_pandora_hmax.jpg' },
  { terms: ['l6503'], path: '/images/itel_l6503_vision_2_3tools_3dumps.jpg' },
  { terms: ['mhorse', 'pop 8'], path: '/images/m_horse_pop8.png' },
  { terms: ['m horse', 'pop 8'], path: '/images/m_horse_pop8.png' },
  { terms: ['infinix hot 40 pro'], path: '/images/infinix_hot40_pro_m_horse.webp' },
  { terms: ['mhorse', 'hot 40 pro', 'v03'], path: '/images/m-horse_hot40pro_v03_unlocktool_hamallah.jpg' },
  { terms: ['m horse', 'hot 40 pro', 'v03'], path: '/images/m-horse_hot40pro_v03_unlocktool_hamallah.jpg' },
  { terms: ['mhorse', 'c55'], path: '/images/m_horse_c55_dual_dump.jpg' },
  { terms: ['m horse', 'c55'], path: '/images/m_horse_c55_dual_dump.jpg' },
  { terms: ['mhorse', 'hot 30'], path: '/images/mhorse_hot_30_full_dump_unlocktool_hamallah.jpg' },
  { terms: ['m horse', 'hot 30'], path: '/images/mhorse_hot_30_full_dump_unlocktool_hamallah.jpg' },
  { terms: ['mhorse', 'spark 10 pro'], path: '/images/m_horse_spark_10_pro_3_versions_full_dump_unlocktool.jpg' },
  { terms: ['m horse', 'spark 10 pro'], path: '/images/m_horse_spark_10_pro_3_versions_full_dump_unlocktool.jpg' },
  { terms: ['oppo a55'], path: '/images/oppo_a55_cph2325_f71_full_dump_4_7gb_pandora_arabic.jpg' },
  { terms: ['cph1933'], path: '/images/oppo_cph1933_a5_2020_full_dump_pandora.jpg' },
  { terms: ['oppo a31'], path: '/images/oppo_a31_cph2015_128gb_emmc_dump.jpg' },
  { terms: ['oppo a54'], path: '/images/oppo_a54_cph2239_dead_boot.jpg' },
  { terms: ['oppo a57'], path: '/images/oppo_a57.jpg' },
  { terms: ['cph2781'], path: '/images/oppo_a6_pro_5g_cph2781.jpg' },
  { terms: ['cph2687'], path: '/images/oppo_reno_12f_4g_cph2687.jpg' },
  { terms: ['rmx3938'], path: '/images/realme_note_60x_rmx3938.jpg' },
  { terms: ['rmx3661'], path: '/images/realme_10_pro_5g_rmx3661.jpg' },
  { terms: ['c35', 'xml'], path: '/images/realme_c35_rmx3511_xml_128gb.jpg' },
  { terms: ['c35'], path: '/images/realme_c35_rmx3511_full_dump_a55_pandora.jpg' },
  { terms: ['rmx3834'], path: '/images/realme_note_50_rmx3834_a89_dump_pandora.jpg' },
  { terms: ['c67', 'copy'], path: '/images/realme_c67_copy_full_dump_pandora_prince_cazanova.jpg' },
  { terms: ['a075f'], path: '/images/samsung_a07_4g_sm_a075f_android16_hmax.jpg' },
  { terms: ['a125f'], path: '/images/samsung_a12_a125f.png' },
  { terms: ['a256e'], path: '/images/samsung_a25_a256e.webp' },
  { terms: ['x110'], path: '/images/samsung_tab_a9_sm_x110_full_dump.jpg' },
  { terms: ['redmi 13c'], path: '/images/xiaomi_redmi_13c_gale_os2_hmax.jpg' },
  { terms: ['beryl'], path: '/images/redmi_note14_5g_beryl_xml_6_5gb_easy_jtag.jpg' },
  { terms: ['redmi a3x'], path: '/images/redmi_a3x_missi_android16_4.5gb.jpg' },
  { terms: ['poco c75'], path: '/images/poco_c75_redmi_14c_17c_a3_pro_1gb_dump_df.jpg' },
  { terms: ['redmi 14c'], path: '/images/poco_c75_redmi_14c_17c_a3_pro_1gb_dump_df.jpg' },
  { terms: ['17c'], path: '/images/poco_c75_redmi_14c_17c_a3_pro_1gb_dump_df.jpg' },
  { terms: ['redmi 15c'], path: '/images/redmi_15c.jpg' },
  { terms: ['vivo y21d'], path: '/images/vivo_y21d_pd2510f.png' },
  { terms: ['vivo y03t'], path: '/images/vivo_y03t_pd2360f.png' },
  { terms: ['vivo y03 4gb'], path: '/images/vivo_y03_dump_4gb_easy_jtag.jpg' },
  { terms: ['vivo y18'], path: '/images/vivo_y18_pd2327f.png' },
  { terms: ['vivo y22s'], path: '/images/vivo_y22s_pd2228f.png' },
  { terms: ['vivo y20s'], path: '/images/vivo_y20s_g_y12s_fake_8_256_unlocktool_nv.jpg' },
  { terms: ['vivo y12s'], path: '/images/vivo_y12s_v2026_pd2036f_unlocktool_nv.jpg' },
  { terms: ['vivo y100'], path: '/images/vivo_y100_v2239_pd2257f_unlocktool_nv.jpg' },
  { terms: ['vivo y53s'], path: '/images/vivo_y53s_v2058_pd2103f_unlocktool_nv.jpg' },
  { terms: ['vivo y75a'], path: '/images/vivo_y75a_unlocktool_nv.jpg' },
  { terms: ['vivo y21 pd'], path: '/images/vivo_y21_pd2139f_unlocktool_nv.jpg' },
  { terms: ['vivo v27e'], path: '/images/vivo_v27e_v2237_unlocktool_nv.jpg' },
  { terms: ['vivo y02s'], path: '/images/vivo_y02s_v2203_pd2216f_unlocktool_nv.jpg' },
  { terms: ['vivo y15s'], path: '/images/vivo_y15s_v2120_pd2140f_2_versions_full_dump_unlocktool.jpg' },
  { terms: ['vivo y1s'], path: '/images/vivo_y1s_pd2014f_unlocktool_nv.jpg' },
  { terms: ['vivo y83'], path: '/images/vivo_y83_pd1803bf_unlocktool_nv.jpg' },
  { terms: ['vivo y27'], path: '/images/vivo_y27_y36_5g_v2248_dump_7_3gb_hmax.jpg' },
  { terms: ['vivo y36'], path: '/images/vivo_y27_y36_5g_v2248_dump_7_3gb_hmax.jpg' },
  { terms: ['vivo y04', 'osv15'], path: '/images/vivo_y04_v2430_2_osv15_easyjtag_khaled_kabo.jpg' },
  { terms: ['vivo y04'], path: '/images/vivo_y04_v2430_latest_10gb_jtag_mustafa.jpg' },
  { terms: ['ytab ultra 35'], path: '/images/ytab_ultra_35_full_dump_cm2_prince_cazanova.jpg' },
  { terms: ['oteeto tab 15'], path: '/images/the_oteeto_tab_15_full_dump_cm2_rare.jpg' },
  { terms: ['moto e13'], path: '/images/motorola_moto_e13_xt2345-4_pandora_hmax_teal.jpg' },
  { terms: ['xt2523 7'], path: '/images/motorola_xt2523_7_moto_e15_5g_full_dump_amt.jpg' },
  { terms: ['iphone 17 pro'], path: '/images/iphone_17_pro_copy_ds_bd2.jpg' },
  { terms: ['iphone 16 pro'], path: '/images/iphone_16_pro_max_copy_mt6735_pandora.jpg' },
  { terms: ['mt6580'], path: '/images/copy_s26_ultra_mt6580_cm2.jpg' },
  { terms: ['ravoz v7'], path: '/images/ravoz_v7_hmax.jpg' },
  { terms: ['tb 7305x'], path: '/images/lenovo_tb_7305x_scatter_hmax.jpg' },
  { terms: ['blu t5'], path: '/images/blu_t5_tigo_t0050tt_hmax_real.jpg' },
  { terms: ['iris 59'], path: '/images/lava_iris_59_le9930_hmax.jpg' },
  { terms: ['nexg n72'], path: '/images/walton_nexg_n72_hmax.jpg' },
  { terms: ['wiko t10'], path: '/images/wiko_t10_full_dump_v01_57_unlocktool_hamallah.jpg' },
  { terms: ['villaon v20'], path: '/images/villaon_v20_full_dump_v01_57_unlocktool_hamallah.jpg' },
  { terms: ['blackview a55'], path: '/images/blackview_a55_hmax.jpg' },
  { terms: ['hisorl t901'], path: '/images/hisorl_t901_full_dump_unlocktool.jpg' },
  { terms: ['hero 60 max'], path: '/images/allcall_hero_60_max_full_dump_unlocktool_rare_hmax.jpg' },
  { terms: ['spark 40 pro', 'km6'], path: '/images/tecno_spark_40_pro_km6_amt.jpg' },
  { terms: ['spark go 1'], path: '/images/tecno_spark_go_1_kl4.jpg' },
];

function normalizeDumpKey(value: string): string {
  return value
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, ' ')
    .trim()
    .replace(/\s+/g, ' ');
}

export function getDumpImage(item: ItemData, sectionKey = ''): string | undefined {
  if (item.image) return item.image;
  const key = normalizeDumpKey(`${sectionKey} ${item.name} ${item.ver ?? ''}`);
  return DUMP_IMAGE_RULES.find((rule) => rule.terms.every((term) => key.includes(term)))?.path;
}

export function getDumpDescription(item: ItemData): string {
  if (item.desc?.trim()) return item.desc.trim();
  return 'الوصف الأصلي غير متوفر في بيانات المشروع لهذا العنصر.';
}

export function withDumpPresentation(item: ItemData, sectionKey = ''): ItemData {
  return {
    ...item,
    image: getDumpImage(item, sectionKey),
    desc: getDumpDescription(item),
  };
}
