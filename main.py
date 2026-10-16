import telebot, os, time, datetime, json
import threading
from telebot import types
from flask import Flask, jsonify, render_template_string, request
from threading import Thread
import re
import firebase_admin
from firebase_admin import credentials, firestore
import hmax_enhancements as hmaxx
import hmax_pro as hmaxpro
import hmax_i18n as hmaxi18n
import hmax_runtime as hmaxruntime


# ===== TECNO 141 MODELS LIBRARY =====
TECNO_DUMPS = {
    "tecno_spark_2_ka7": {"name": "TECNO SPARK 2 KA7", "url": "https://drive.google.com/drive/folders/1-m9ZynYe8S9dI8G_bU7OtPiqTkg1wlgl"},
    "tecno_spark_3_kb3": {"name": "TECNO SPARK 3 KB3", "url": "https://drive.google.com/drive/folders/1-vgXzJSKVqeTvZgAxc5ztZ7_AxLq9FbJ"},
    "tecno_spark_3_pro_kb8": {"name": "TECNO SPARK 3 Pro KB8", "url": "https://drive.google.com/drive/folders/100BGo4AOd-8UmU5Ij5WYIddE4AmA37XQ"},
    "tecno_spark_4_kc2": {"name": "TECNO SPARK 4 KC2", "url": "https://drive.google.com/drive/folders/10JG6dA0TSAysiPcG4jUczaieu0URoZw7"},
    "tecno_spark_4_air_kc1": {"name": "TECNO SPARK 4 Air KC1", "url": "https://drive.google.com/drive/folders/11dkP5rt3dg7G4H7X4Hw9TBWxx30GoH4m"},
    "tecno_spark_5_kd7": {"name": "TECNO SPARK 5 KD7", "url": "https://drive.google.com/drive/folders/12XiKIypdVAqgmfIwe2flztLkV46Uan7P"},
    "tecno_spark_5_air_kd6": {"name": "TECNO SPARK 5 Air KD6", "url": "https://drive.google.com/drive/folders/133Y_Xlfj7OGXevOaTJ1ZYYQlQnLcqQ2_"},
    "tecno_spark_5_pro_kd7h": {"name": "TECNO SPARK 5 Pro KD7H", "url": "https://drive.google.com/drive/folders/13TGqSs7VXc6eA333_ZFlBQKpYThnmKCA"},
    "tecno_spark_6_ke7": {"name": "TECNO SPARK 6 KE7", "url": "https://drive.google.com/drive/folders/13wS_X7Ujn0IhfdjAbudlBVSLxMXdf9t2"},
    "tecno_spark_6_air_ke6": {"name": "TECNO SPARK 6 Air KE6", "url": "https://drive.google.com/drive/folders/14Rm5LKK7359tMW0Q-cs7WmZ2sPHkdYo_"},
    "tecno_spark_6_go_ke5": {"name": "TECNO SPARK 6 Go KE5", "url": "https://drive.google.com/drive/folders/15JF_3ySQUmoeoh96cFlyW_azy2s0Qccq"},
    "tecno_spark_7_kf6": {"name": "TECNO SPARK 7 KF6", "url": "https://drive.google.com/drive/folders/15yVmCNTjkvYYYXiJ8n0T9sskRRQj9ZQw"},
    "tecno_spark_7p_kf7j": {"name": "TECNO SPARK 7P KF7J", "url": "https://drive.google.com/drive/folders/166s4XVMuDiPJl9xmYn_WAGV1T_CdwLr4"},
    "tecno_spark_7t_kf6p": {"name": "TECNO SPARK 7T KF6P", "url": "https://drive.google.com/drive/folders/16BWgqWtMoM50BYzEQHPQBzwt0ljzK5Bs"},
    "tecno_spark_8_kg6": {"name": "TECNO SPARK 8 KG6", "url": "https://drive.google.com/drive/folders/16jLxWX-gPhuRTpBFU1ChqXe6sWyP-T0F"},
    "tecno_spark_8c_kg5": {"name": "TECNO SPARK 8C KG5", "url": "https://drive.google.com/drive/folders/16nTXFprwhJQjlDZ0r-W5_0l-BUTRrRdg"},
    "tecno_spark_8p_kg7h": {"name": "TECNO SPARK 8P KG7H", "url": "https://drive.google.com/drive/folders/179vJDld7mv8Z4kL2ZGtLyYOmhezD-t-x"},
    "tecno_spark_8t_kg6p": {"name": "TECNO SPARK 8T KG6P", "url": "https://drive.google.com/drive/folders/18v-IQXQEL1T5fibe9uFoYNs1mwMAt9yT"},
    "tecno_spark_9_kg10": {"name": "TECNO SPARK 9 KG10", "url": "https://drive.google.com/drive/folders/19Xe2usg_tmOXJH2KInS-F0qmx6w7z3Y1"},
    "tecno_spark_9t_kh6": {"name": "TECNO SPARK 9T KH6", "url": "https://drive.google.com/drive/folders/1A3TzPyZQY332aXRghkyL_9PYDQ9XjLzt"},
    "tecno_spark_9_pro_kh7": {"name": "TECNO SPARK 9 Pro KH7", "url": "https://drive.google.com/drive/folders/1ANiLQQ2_bSrfXGUvhB_GavjnRkvJBpBq"},
    "tecno_spark_10_ki5": {"name": "TECNO SPARK 10 KI5", "url": "https://drive.google.com/drive/folders/1AtObtnhdv4KsAiPLxltE4EicTyL0rbYJ"},
    "tecno_spark_10c_ki5k": {"name": "TECNO SPARK 10C KI5K", "url": "https://drive.google.com/drive/folders/1B1fRzLijaye9X7pWEIcvVW_-bVHTdXx6"},
    "tecno_spark_10_pro_ki7": {"name": "TECNO SPARK 10 Pro KI7", "url": "https://drive.google.com/drive/folders/1B6mUpM8zG2s4g9XUrRqH__iDtYYtkH1m"},
    "tecno_spark_10t_ki5t": {"name": "TECNO SPARK 10T KI5T", "url": "https://drive.google.com/drive/folders/1BIdsD8VvSqF12mUDhZ0jOwwmcen8DNeI"},
    "tecno_spark_20_kj5": {"name": "TECNO SPARK 20 KJ5", "url": "https://drive.google.com/drive/folders/1BOZ_TRuxytEktE7KzetkLGfu-W-A31Ke"},
    "tecno_spark_20c_bg7": {"name": "TECNO SPARK 20C BG7", "url": "https://drive.google.com/drive/folders/1BTpcU4CcuLKdjc6c6mrhUy-MhtjUzcxn"},
    "tecno_spark_20_pro_kj6": {"name": "TECNO SPARK 20 Pro KJ6", "url": "https://drive.google.com/drive/folders/1C1Dy3CqiWhtmpeD7IhE14fKy2UPdir45"},
    "tecno_spark_20_proplus_kj7": {"name": "TECNO SPARK 20 Pro+ KJ7", "url": "https://drive.google.com/drive/folders/1C7lwkjCxl3fEi1WQyQb3J9DhD24nV1E_"},
    "tecno_spark_go_2020_ke5j": {"name": "TECNO SPARK Go 2020 KE5J", "url": "https://drive.google.com/drive/folders/1CXDyNx7_vafU9-AA2NWBM68_zOCGRs37"},
    "tecno_spark_go_2021_ke5k": {"name": "TECNO SPARK Go 2021 KE5K", "url": "https://drive.google.com/drive/folders/1D6qrusumdFXMQof2R2ab2hwE4QTwHmId"},
    "tecno_spark_go_2022_kg5a": {"name": "TECNO SPARK Go 2022 KG5A", "url": "https://drive.google.com/drive/folders/1DJk3VhPoo11D197NfhyAn1b1qR1YQgHk"},
    "tecno_spark_go_2023_bf7": {"name": "TECNO SPARK Go 2023 BF7", "url": "https://drive.google.com/drive/folders/1DRuZfy4O3LdvAwHxrc901ocf_D58W4gj"},
    "tecno_spark_go_2024_bg6": {"name": "TECNO SPARK Go 2024 BG6", "url": "https://drive.google.com/drive/folders/1D_KXbos9taI9TfXzOsumHsDIluakoD8a"},
    "tecno_spark_40_kl5": {"name": "TECNO SPARK 40 KL5", "url": "https://drive.google.com/drive/folders/1DdzE_ZeytpSUnY2KqsiOdSBzb44iov1Q"},
    "tecno_spark_40_pro_km6": {"name": "TECNO SPARK 40 Pro KM6", "url": "https://drive.google.com/drive/folders/1DqVSTBr0tVeSEtpnZ6_C7BzOHj_3OkzW"},
    "tecno_spark_40_proplus_km7": {"name": "TECNO SPARK 40 Pro+ KM7", "url": "https://drive.google.com/drive/folders/1EIrAZ0WC7b7_1SX_C5JKHuLiU9PQNr_a"},
    "tecno_camon_11_cf7": {"name": "TECNO CAMON 11 CF7", "url": "https://drive.google.com/drive/folders/1EgJaPwILRLezqUNJBiLcDuceth2QEemT"},
    "tecno_camon_11_pro_cf8": {"name": "TECNO CAMON 11 Pro CF8", "url": "https://drive.google.com/drive/folders/1En3QMKRLs86WQ7rVsZq-waZSiHT-zoRc"},
    "tecno_camon_12_cc7": {"name": "TECNO CAMON 12 CC7", "url": "https://drive.google.com/drive/folders/1F70V8JGMSBfurVOu_hxoFT1Bi8Bi84fp"},
    "tecno_camon_12_air_cc6": {"name": "TECNO CAMON 12 Air CC6", "url": "https://drive.google.com/drive/folders/1G1jf_9jSOMoAcSfO1FBRRcsDz1TxpW-R"},
    "tecno_camon_12_pro_cc9": {"name": "TECNO CAMON 12 Pro CC9", "url": "https://drive.google.com/drive/folders/1GbCaREdOSHXjJkcGwmXA7otBLLGz78RB"},
    "tecno_camon_15_cd7": {"name": "TECNO CAMON 15 CD7", "url": "https://drive.google.com/drive/folders/1Ge92FTek3V7wiZNm-68plo5MvJir0evK"},
    "tecno_camon_15_air_cd6": {"name": "TECNO CAMON 15 Air CD6", "url": "https://drive.google.com/drive/folders/1GkV2AlbKSA4JfnIhUUtFTqtCdPsvM9ww"},
    "tecno_camon_15_pro_cd8": {"name": "TECNO CAMON 15 Pro CD8", "url": "https://drive.google.com/drive/folders/1HfDnMnZ7Hd9UeM5DeDZ6xu4LZumDaxiq"},
    "tecno_camon_16_ce7": {"name": "TECNO CAMON 16 CE7", "url": "https://drive.google.com/drive/folders/1IF7wNE1POKbBcYmTDbwjAvlX2q78V3XW"},
    "tecno_camon_16_pro_ce8": {"name": "TECNO CAMON 16 Pro CE8", "url": "https://drive.google.com/drive/folders/1IjwY4qrA5iLCtnwc0e5wYUCcExtFmYCr"},
    "tecno_camon_16_premier_ce9": {"name": "TECNO CAMON 16 Premier CE9", "url": "https://drive.google.com/drive/folders/1Js9pYoralgMhLlDhZ_gGfExDhdxzMwLC"},
    "tecno_camon_17_cg6": {"name": "TECNO CAMON 17 CG6", "url": "https://drive.google.com/drive/folders/1L1MIMkaHU-IbW2v9uymQxcaE0_0XQxmq"},
    "tecno_camon_17_pro_cg7": {"name": "TECNO CAMON 17 Pro CG7", "url": "https://drive.google.com/drive/folders/1LxXDNnMg4D5ztqJLrSORG6swNl8yg5ef"},
    "tecno_camon_17p_cg7s": {"name": "TECNO CAMON 17P CG7S", "url": "https://drive.google.com/drive/folders/1MCDr3yYTWQzLkBOh9lYWu6zJAM5rW30K"},
    "tecno_camon_18_ch6": {"name": "TECNO CAMON 18 CH6", "url": "https://drive.google.com/drive/folders/1N29KtZ55cWdj5-CCelL5gLDCzqtdb-qG"},
    "tecno_camon_18p_ch7": {"name": "TECNO CAMON 18P CH7", "url": "https://drive.google.com/drive/folders/1N3qhvJhcmxg4CrSVmpN-xwWfP6XOUMan"},
    "tecno_camon_18_premier_ch9": {"name": "TECNO CAMON 18 Premier CH9", "url": "https://drive.google.com/drive/folders/1NOkjzkgtpdsCcmYSoyKn0TeJS3FufJRD"},
    "tecno_camon_19_ci6": {"name": "TECNO CAMON 19 CI6", "url": "https://drive.google.com/drive/folders/1Oogz7PC5JuSeXDzc_YIVe6ZMv8QeYWTl"},
    "tecno_camon_19_pro_ci7": {"name": "TECNO CAMON 19 Pro CI7", "url": "https://drive.google.com/drive/folders/1PMf3SFB-w97nEFSD7SKLVxtPAFVcLyHR"},
    "tecno_camon_19_neo_ci6s": {"name": "TECNO CAMON 19 Neo CI6S", "url": "https://drive.google.com/drive/folders/1PU3A1x-9ciWjbgMgMtkw2gbcuV44PeCd"},
    "tecno_camon_19_pro_5g_ci7n": {"name": "TECNO CAMON 19 Pro 5G CI7N", "url": "https://drive.google.com/drive/folders/1PZKt-Xq_XPmM5SzxsoiI6oZ0lTYC_NbB"},
    "tecno_camon_20_ck6": {"name": "TECNO CAMON 20 CK6", "url": "https://drive.google.com/drive/folders/1PgU9O2Zskj9pNYEIvnBJXIcNUPNk_e9o"},
    "tecno_camon_20_pro_ck7": {"name": "TECNO CAMON 20 Pro CK7", "url": "https://drive.google.com/drive/folders/1PmZkaGMt7QwKEgCWjX5IcySLbkQT_8-R"},
    "tecno_camon_20_pro_5g_ck8": {"name": "TECNO CAMON 20 Pro 5G CK8", "url": "https://drive.google.com/drive/folders/1QK9zkmewm6wYm-ijZ0Fn3wrpU3z0XhZk"},
    "tecno_camon_20_premier_ck9": {"name": "TECNO CAMON 20 Premier CK9", "url": "https://drive.google.com/drive/folders/1Qb08q0gLLjRRqBQtWGgo8XwLrVywBJag"},
    "tecno_camon_30_cl6": {"name": "TECNO CAMON 30 CL6", "url": "https://drive.google.com/drive/folders/1SWp8MskCdmM0w271E1Bm6cmRQTKV1VTd"},
    "tecno_camon_30_pro_cl7": {"name": "TECNO CAMON 30 Pro CL7", "url": "https://drive.google.com/drive/folders/1Soku2BdxP4F5CU3w7rVYfVSdNIwwydjV"},
    "tecno_camon_30_5g_cl6k": {"name": "TECNO CAMON 30 5G CL6K", "url": "https://drive.google.com/drive/folders/1SrYkhvbZYH_ftz3UQM_W7RUV2xPt4o-N"},
    "tecno_camon_30_premier_cl9": {"name": "TECNO CAMON 30 Premier CL9", "url": "https://drive.google.com/drive/folders/1T9CHlE2Bu3wqlGj8XzvgFw2ZbcQwyzpN"},
    "tecno_camon_40_cm5": {"name": "TECNO CAMON 40 CM5", "url": "https://drive.google.com/drive/folders/1TSIAMGesn5dm0eBLXKRroWu1vIcyUYmS"},
    "tecno_camon_40_pro_cm6": {"name": "TECNO CAMON 40 Pro CM6", "url": "https://drive.google.com/drive/folders/1TSY4ypTu_VW0qxhbUuSYxMM7v067g65k"},
    "tecno_camon_40_pro_5g_cm7": {"name": "TECNO CAMON 40 Pro 5G CM7", "url": "https://drive.google.com/drive/folders/1TUHgVOOuTD36wangf2t2SWfm95zKDszC"},
    "tecno_pova_ld7": {"name": "TECNO POVA LD7", "url": "https://drive.google.com/drive/folders/1TUKIpMGs3N8E72-s3NjfLTdKX_UHWAkC"},
    "tecno_pova_2_le7": {"name": "TECNO POVA 2 LE7", "url": "https://drive.google.com/drive/folders/1TqPyN9Tu0QNT9xCY0a-nlckxfgUadhxF"},
    "tecno_pova_3_lf7": {"name": "TECNO POVA 3 LF7", "url": "https://drive.google.com/drive/folders/1U-iyUYdZSoG1tNlKbn7abn3jmb8NWB7T"},
    "tecno_pova_4_lg6": {"name": "TECNO POVA 4 LG6", "url": "https://drive.google.com/drive/folders/1Uby3PRJ1y2kNzRq_b0cFGu9rdAmaWm5b"},
    "tecno_pova_4_pro_lg8": {"name": "TECNO POVA 4 Pro LG8", "url": "https://drive.google.com/drive/folders/1Ue7ghoXDkRPDqAFkhNp4Uig8v7Tgzo-M"},
    "tecno_pova_5_lh6": {"name": "TECNO POVA 5 LH6", "url": "https://drive.google.com/drive/folders/1UzcWfXVs7tvdsF3zaZ-oQHsTM1w4cFB9"},
    "tecno_pova_5_pro_lh8": {"name": "TECNO POVA 5 Pro LH8", "url": "https://drive.google.com/drive/folders/1VHB_2vcwsLHRBv4bwyb0OwpANgh_p8Yj"},
    "tecno_pova_6_li6": {"name": "TECNO POVA 6 LI6", "url": "https://drive.google.com/drive/folders/1W1WrXoLCrnXuGwVLrZKtZElDOI-qmiY1"},
    "tecno_pova_6_pro_li8": {"name": "TECNO POVA 6 Pro LI8", "url": "https://drive.google.com/drive/folders/1WUS5Htr9HKfZSC3X2ix8sZseyHxNr6Ey"},
    "tecno_pova_neo_le6": {"name": "TECNO POVA Neo LE6", "url": "https://drive.google.com/drive/folders/1Wlx97JQPXcr6UOnSfxcoNg5PMaBsnYx3"},
    "tecno_pova_neo_2_lg6n": {"name": "TECNO POVA Neo 2 LG6N", "url": "https://drive.google.com/drive/folders/1WwDRbCtlGW3hqPXKq5RyFRdOcBlmqtqy"},
    "tecno_pova_neo_3_le6s": {"name": "TECNO POVA Neo 3 LE6S", "url": "https://drive.google.com/drive/folders/1X3j2ps9BUKabqKGNvrEWxB5yx65YJz2M"},
    "tecno_pop_2_b1": {"name": "TECNO POP 2 B1", "url": "https://drive.google.com/drive/folders/1XcOpSv2VT06_TRsTUy_OV6Lx-bStUt-k"},
    "tecno_pop_2f_b1f": {"name": "TECNO POP 2F B1F", "url": "https://drive.google.com/drive/folders/1XiqgNIWzb2f0NUS6LqRZR56ZF4n9xBo3"},
    "tecno_pop_2_power_b1p": {"name": "TECNO POP 2 Power B1P", "url": "https://drive.google.com/drive/folders/1XsLIkhWWT2CcxJWu5JwLKJFJn0avvil7"},
    "tecno_pop_3_bb2": {"name": "TECNO POP 3 BB2", "url": "https://drive.google.com/drive/folders/1XvdOQdzHOTd3ID3jaIuJk1Jeq-G5ALbv"},
    "tecno_pop_4_bc2": {"name": "TECNO POP 4 BC2", "url": "https://drive.google.com/drive/folders/1XzL99j2NoLpTCLjHCj5uWdu-ivoHouL4"},
    "tecno_pop_4_air_bc1": {"name": "TECNO POP 4 Air BC1", "url": "https://drive.google.com/drive/folders/1Y3CIQlAoSi8328AuT36NZdrCzxxfv60a"},
    "tecno_pop_5_bd2": {"name": "TECNO POP 5 BD2", "url": "https://drive.google.com/drive/folders/1YHq7GwqDLoRAHUlENzWMC51GMegjtCEW"},
    "tecno_pop_5_lte_bd4": {"name": "TECNO POP 5 LTE BD4", "url": "https://drive.google.com/drive/folders/1YPiu-vapMTL960vE9rdce5D7shBrP3yz"},
    "tecno_pop_5_go_bd1": {"name": "TECNO POP 5 Go BD1", "url": "https://drive.google.com/drive/folders/1YYPHeGty78_SBrn2qDCFu08kQDnyznqI"},
    "tecno_pop_6_be7": {"name": "TECNO POP 6 BE7", "url": "https://drive.google.com/drive/folders/1Yfp9Cj3hvE2vdEVxTe0qLw9rPocK7NcX"},
    "tecno_pop_6_go_be6": {"name": "TECNO POP 6 Go BE6", "url": "https://drive.google.com/drive/folders/1_T3F4BFVYFXg-qF4f0MTvtzuElzDzxaR"},
    "tecno_pop_7_bf6": {"name": "TECNO POP 7 BF6", "url": "https://drive.google.com/drive/folders/1_jMnJeKNEr0Kgxd2ydUOOIcKp4zMALY3"},
    "tecno_pop_7_pro_bf7h": {"name": "TECNO POP 7 Pro BF7H", "url": "https://drive.google.com/drive/folders/1_w5Yl_YVMFa4QI5QADZPgP_nuzr4qTqh"},
    "tecno_pop_8_bg6": {"name": "TECNO POP 8 BG6", "url": "https://drive.google.com/drive/folders/1afEUxMLViJWmP5u7_UQXzrq0QiMp6y-D"},
    "tecno_pop_9_bg8": {"name": "TECNO POP 9 BG8", "url": "https://drive.google.com/drive/folders/1anFAH8BvWXw5_fncRu6gZ0m4SNO_hDaC"},
    "tecno_phantom_6_a6": {"name": "TECNO PHANTOM 6 A6", "url": "https://drive.google.com/drive/folders/1cFn6IPYeZGpHxnj4u9qwtYJSg6TB5pJN"},
    "tecno_phantom_6_plus_a9": {"name": "TECNO PHANTOM 6 Plus A9", "url": "https://drive.google.com/drive/folders/1cQA7kiXQPjRbpLli4ccBkFp_r4EkAUYK"},
    "tecno_phantom_8_ax8": {"name": "TECNO PHANTOM 8 AX8", "url": "https://drive.google.com/drive/folders/1cXHqpQMT-_FhencX0moRlBiQ5yQ4fuPr"},
    "tecno_phantom_9_ab7": {"name": "TECNO PHANTOM 9 AB7", "url": "https://drive.google.com/drive/folders/1cxIxNMh9yBwEWLFWy1HPWwmMAkYdKTZA"},
    "tecno_phantom_x_ac8": {"name": "TECNO PHANTOM X AC8", "url": "https://drive.google.com/drive/folders/1e2lYtYkZINZjjxKVctz3nJ6c53KlDTmD"},
    "tecno_phantom_x2_ad8": {"name": "TECNO PHANTOM X2 AD8", "url": "https://drive.google.com/drive/folders/1eJ-IeCyFFZ3QfCu7HvtOEsAmb7BcNOeJ"},
    "tecno_phantom_x2_pro_ad9": {"name": "TECNO PHANTOM X2 Pro AD9", "url": "https://drive.google.com/drive/folders/1eJoaxxnI7gbPonJe5AxzhDGs0chwS6_L"},
    "tecno_phantom_v_fold_ad10": {"name": "TECNO PHANTOM V Fold AD10", "url": "https://drive.google.com/drive/folders/1f5AcRbxawfIYZEBSQlxjt_pHtogX5qZu"},
    "tecno_phantom_v_flip_ad11": {"name": "TECNO PHANTOM V Flip AD11", "url": "https://drive.google.com/drive/folders/1f_irEyI_ZAK9320eU9MN8MRwppgkVc8H"},
    "tecno_camon_i_in1": {"name": "TECNO CAMON i IN1", "url": "https://drive.google.com/drive/folders/1g8h21VBnGY41j_ePj14EL08XmW-OqMwK"},
    "tecno_camon_i2_id5": {"name": "TECNO CAMON i2 ID5", "url": "https://drive.google.com/drive/folders/1gXfF2ZZ2sh0EJm7imyUmDuYhf0Be78_U"},
    "tecno_camon_i2x_id5a": {"name": "TECNO CAMON i2X ID5A", "url": "https://drive.google.com/drive/folders/1ghOf2LWJfnnCBMJTy-YyVxABhUfqk07k"},
    "tecno_camon_i4_cb7": {"name": "TECNO CAMON i4 CB7", "url": "https://drive.google.com/drive/folders/1h1F1oMpBzdk7LtmnoF6wa8ZH90jeBEOw"},
    "tecno_camon_iclick_in6": {"name": "TECNO CAMON iClick IN6", "url": "https://drive.google.com/drive/folders/1hC3SExzTxBtig_5QEDk8ACDsS0wPIr9g"},
    "tecno_camon_cx_cc5": {"name": "TECNO CAMON CX CC5", "url": "https://drive.google.com/drive/folders/1iPD3U-Gy8QRMR4aIfiDpOdQGAh--n-Mj"},
    "tecno_camon_cm_ca6": {"name": "TECNO CAMON CM CA6", "url": "https://drive.google.com/drive/folders/1jCPkzP-8YuW7Zywln1JVTAJBHLpR4Pd0"},
    "tecno_camon_c8_c8": {"name": "TECNO CAMON C8 C8", "url": "https://drive.google.com/drive/folders/1jsGTx_JTCNIQnmXw2dDAo0UgPxGbK5ok"},
    "tecno_camon_c9_c9": {"name": "TECNO CAMON C9 C9", "url": "https://drive.google.com/drive/folders/1kTU_3fttuP4Gq5ZvB99vkFoEoOQDWiyd"},
    "tecno_wx3_wx3": {"name": "TECNO WX3 WX3", "url": "https://drive.google.com/drive/folders/1lhkiAMH8yub61EesvZQz9AAz_19KCepG"},
    "tecno_wx4_wx4": {"name": "TECNO WX4 WX4", "url": "https://drive.google.com/drive/folders/1mWOpulIdNcOjCA9FlbRknrQnfbo_R7ua"},
    "tecno_w1_w1": {"name": "TECNO W1 W1", "url": "https://drive.google.com/drive/folders/1n7htCb91mB0ewlbRBNfklq__wz0Es4f7"},
    "tecno_w2_w2": {"name": "TECNO W2 W2", "url": "https://drive.google.com/drive/folders/1nnXvU52FrCaUQe6gUH45TZFpo6KPflPD"},
    "tecno_w3_w3": {"name": "TECNO W3 W3", "url": "https://drive.google.com/drive/folders/1nooB25MuhICQvAAUqG_NsubKmPJso7uX"},
    "tecno_w5_w5": {"name": "TECNO W5 W5", "url": "https://drive.google.com/drive/folders/1o3_P8i2VQcDJR7Ceb1Jk5Y4l_0p_KSDY"},
    "tecno_l8_l8": {"name": "TECNO L8 L8", "url": "https://drive.google.com/drive/folders/1o7xBTah4TNngTb8NJmOshk_hW-oj3P60"},
    "tecno_l9_plus_l9p": {"name": "TECNO L9 Plus L9P", "url": "https://drive.google.com/drive/folders/1oiw6CekpmI_5a0LQcbS4AXCTrGUgaOEP"},
    "tecno_f1_f1": {"name": "TECNO F1 F1", "url": "https://drive.google.com/drive/folders/1opniGT7fQFE7HNrPbo_eU5TsBDQvukz5"},
    "tecno_f2_f2": {"name": "TECNO F2 F2", "url": "https://drive.google.com/drive/folders/1p82ycxTBXapuOp7GfLjZ6I2NkQZ7JYNN"},
    "tecno_sa1s_sa1s": {"name": "TECNO SA1S SA1S", "url": "https://drive.google.com/drive/folders/1pW14QX2HFu9OJVtA-8SQePpOLX1ebBHB"},
    "tecno_kg5p_spark_go_2022": {"name": "TECNO KG5P SPARK Go 2022", "url": "https://drive.google.com/drive/folders/1pbx7dbOiKByjp91azZOZNKIKs_JQmxOU"},
    "tecno_kg7_spark_8p": {"name": "TECNO KG7 SPARK 8P", "url": "https://drive.google.com/drive/folders/1qcKTvJd4hBHDxOb64KnqKbLJIV9xkfO0"},
    "tecno_ki7s_spark_10_pro_magic": {"name": "TECNO KI7S SPARK 10 Pro Magic", "url": "https://drive.google.com/drive/folders/1rh6MrMKGWRQpblnnFgD99VnTEkyNEMeC"},
    "tecno_lh7n_pova_5_pro_5g": {"name": "TECNO LH7N POVA 5 Pro 5G", "url": "https://drive.google.com/drive/folders/1smKi3GKpYQ38qba6QAzvoiQKM-fnhlhJ"},
    "tecno_cl8_camon_30s": {"name": "TECNO CL8 CAMON 30S", "url": "https://drive.google.com/drive/folders/1ujOIZetpCF8LDzPA2h9xjcWFk76A0y7p"},
    "tecno_kl4_spark_40c": {"name": "TECNO KL4 SPARK 40C", "url": "https://drive.google.com/drive/folders/1un4LGdDRfu-wp41gzT8AjNMYxqWs91UQ"},
    "tecno_km5_spark_40": {"name": "TECNO KM5 SPARK 40", "url": "https://drive.google.com/drive/folders/1wGRPHLwQGUWfNVBzSUUqNZD5HJrgpKuI"},
    "tecno_li9_pova_6_neo": {"name": "TECNO LI9 POVA 6 Neo", "url": "https://drive.google.com/drive/folders/1wn-NWGsD4485xfkBS_mBI9EsrS3lOqC4"},
    "tecno_bf6_pop_7": {"name": "TECNO BF6 POP 7", "url": "https://drive.google.com/drive/folders/1wpb569X4ljOHme4Z_8g4Pueaj2WqBAFZ"},
    "tecno_bg6m_pop_8": {"name": "TECNO BG6M POP 8", "url": "https://drive.google.com/drive/folders/1xOxdR5dx7ISLQFFpbIE0HYkF_UXrDOqh"},
    "tecno_ad12_phantom_v2_fold": {"name": "TECNO AD12 PHANTOM V2 Fold", "url": "https://drive.google.com/drive/folders/1xWcwiB_4i6wms_fpBsd6YMsv7IoX_Rw1"},
    "tecno_spark_10_5g_ki8": {"name": "TECNO SPARK 10 5G KI8", "url": "https://drive.google.com/drive/folders/1yDJP0eRcWy7mm8h1WSww9QBVemI9ZRgb"},
    "tecno_spark_20_pro_5g_kj8": {"name": "TECNO SPARK 20 Pro 5G KJ8", "url": "https://drive.google.com/drive/folders/1yw7gCCzm-SkN5FAcRpuu7QE1ZlDx4DM_"},
    "tecno_camon_19_pro_mondrian": {"name": "TECNO CAMON 19 Pro Mondrian", "url": "https://drive.google.com/drive/folders/1z1NI5Orbd4XZmVfdZVEJfZGB33d_HGcY"},
    "tecno_pova_curve_li8s": {"name": "TECNO POVA Curve LI8S", "url": "https://drive.google.com/drive/folders/1zH2J5-kn7wemLKmUydwlwgxEpaxBTzyw"},
    "tecno_zybiq2eqxxkjt6tpq2t_gutwfv0qphss": {"name": "TECNO Additional Model", "url": "https://drive.google.com/drive/folders/1zyBIQ2EqxxkJT6tpQ2t_gutwfV0qPHSS"},
}

TECNO_PAGE_SIZE = 20  # عدد موديلات TECNO في كل صفحة


# English / French captions of DUMP model cards, keyed by callback_data.
# Arabic stays in the handler and is used for ar (and for any missing entry).
_DUMP_CARD_TEXT = {
    "dump_model_allcall_hero_60_max_full_dump_unlocktool": {"en": "🔥 *A very rare file just arrived, for AllCall Hero 60 Max!*\n━━━━━━━━━━━━\n📱 AllCall Hero 60 Max — FULL DUMP\n━━━━━━━━━━━━\nIf you are looking for firmware for this device, you probably know that rare files make all the difference when the device is in front of you and no file is available.\n━━━━━━━━━━━━\n🔧 **The file was read directly from the device using UnlockTool**, then uploaded and prepared for download via Google Drive.\n━━━━━━━━━━━━\n📦 Firmware details:\n• Model: AllCall Hero 60 Max\n• Type: Full Dump\n• Tool: UnlockTool\n• Hosting: Google Drive\n• Password: MobiFirmware.VIP\n━━━━━━━━━━━━\n💎 A dump you will never find online in the form available here.\n━━━━━━━━━━━━\nHMAX-UNLOCKER • HithamMax", "fr": "🔥 *Un fichier très rare vient d’arriver pour l’AllCall Hero 60 Max !*\n━━━━━━━━━━━━\n📱 AllCall Hero 60 Max — FULL DUMP\n━━━━━━━━━━━━\nSi vous cherchez un firmware pour cet appareil, vous savez sans doute que les fichiers rares font toute la différence quand l’appareil est devant vous et qu’aucun fichier n’est disponible.\n━━━━━━━━━━━━\n🔧 **Le fichier a été extrait directement de l’appareil avec UnlockTool**, puis mis en ligne et préparé pour le téléchargement via Google Drive.\n━━━━━━━━━━━━\n📦 Détails du firmware :\n• Modèle : AllCall Hero 60 Max\n• Type : Full Dump\n• Outil : UnlockTool\n• Hébergement : Google Drive\n• Mot de passe : MobiFirmware.VIP\n━━━━━━━━━━━━\n💎 Un dump que vous ne trouverez jamais en ligne sous la forme proposée ici.\n━━━━━━━━━━━━\nHMAX-UNLOCKER • HithamMax"},
    "dump_model_benco_s1_pro_ae9260_dual": {"en": "⭐ BENCO S1 Pro — AE9260 — DUAL FULL DUMP 🔥\n━━━━━━━━━━━━\n📁 We offer more than one dump option so the technician can find the right solution\n━━━━━━━━━━━━\n📁 Dump 1 | Pandora Tool:\nBenco S1 Pro AE9260 - S174-24F25 Lava Dump By Pandora\n━━━━━━━━━━━━\n📁 Dump 2 | CM2:\nBENCO_S1_PRO_UMS9230_INONE_AE9260_OSv13_benco_AE9260_S174_24F25 FULL DUMP BY CM2\n━━━━━━━━━━━━\n🔧 Tools: Pandora Tool + CM2\n🔐 Pass: MobiFirmware.VIP\n💡 Feature: several options for the same device = more flexibility", "fr": "⭐ BENCO S1 Pro — AE9260 — DUAL FULL DUMP 🔥\n━━━━━━━━━━━━\n📁 Nous proposons plusieurs options de dump pour que le technicien trouve la solution adaptée\n━━━━━━━━━━━━\n📁 Dump 1 | Pandora Tool :\nBenco S1 Pro AE9260 - S174-24F25 Lava Dump By Pandora\n━━━━━━━━━━━━\n📁 Dump 2 | CM2 :\nBENCO_S1_PRO_UMS9230_INONE_AE9260_OSv13_benco_AE9260_S174_24F25 FULL DUMP BY CM2\n━━━━━━━━━━━━\n🔧 Outils : Pandora Tool + CM2\n🔐 Mot de passe : MobiFirmware.VIP\n💡 Atout : plusieurs options pour le même appareil = plus de souplesse"},
    "dump_model_benco_v60_full": {"en": "📱 Benco V60 — FULL DUMP 🔥\n━━━━━━━━━━━━\nNot every device has a ready dump when you need it...\nThat is why we keep preparing the files technicians need.\n━━━━━━━━━━━━\n📱 Device: Benco V60\n🔧 Read By: CM2\n📁 File: Full Dump\n☁️ Hosting: Google Drive\n🔐 Pass: MobiFirmware.VIP", "fr": "📱 Benco V60 — FULL DUMP 🔥\n━━━━━━━━━━━━\nTous les appareils n’ont pas de dump prêt quand on en a besoin...\nC’est pourquoi nous continuons à préparer les fichiers dont les techniciens ont besoin.\n━━━━━━━━━━━━\n📱 Appareil : Benco V60\n🔧 Extrait avec : CM2\n📁 Fichier : Full Dump\n☁️ Hébergement : Google Drive\n🔐 Mot de passe : MobiFirmware.VIP"},
    "dump_model_copy_s26_ultra_mt6580": {"en": "⚠️ New dump for COPY devices | Warning ⚠️\n━━━━━━━━━━━━\nThe device is labelled as an S25 Ultra\nThe device itself says: wait... I am an S26 Ultra!\nIn short: the box says one thing and the device is another!\n━━━━━━━━━━━━\n📊 DUMP INFORMATION\nProduct Model: S26 Ultra\nBrand: alps\nProduct Name: S26_Ultra\nProduct Device: S26_Ultra\nCPU: MT6580\nBoard: k80hd_bsp_fwv_512m\nPlatform: MT6580\nAndroid: 8.1.0\nPatch Level: O11019\nSecurity Patch: 2021-03-05\nDisplay ID: V207-Q16-MC-Q26-20260114\nSW Version: 1768383878\nBuild Time: 14/01/2026 09:44:30 AM\nArchitecture: armeabi-v7a / armeabi\nDump: FULL DUMP\nTool: CM2\n━━━━━━━━━━━━\n🔐 Pass: MobiFirmware.VIP", "fr": "⚠️ Nouveau dump pour les appareils COPY | Attention ⚠️\n━━━━━━━━━━━━\nL’appareil se présente comme un S25 Ultra\nL’appareil lui-même dit : attendez... je suis un S26 Ultra !\nEn résumé : ce qui est écrit sur la boîte n’est pas ce que contient l’appareil !\n━━━━━━━━━━━━\n📊 INFORMATIONS DU DUMP\nModèle produit : S26 Ultra\nMarque : alps\nNom du produit : S26_Ultra\nAppareil produit : S26_Ultra\nProcesseur : MT6580\nCarte : k80hd_bsp_fwv_512m\nPlateforme : MT6580\nAndroid : 8.1.0\nPatch Level : O11019\nCorrectif de sécurité : 2021-03-05\nID d’affichage : V207-Q16-MC-Q26-20260114\nVersion SW : 1768383878\nDate de build : 14/01/2026 09:44:30 AM\nArchitecture : armeabi-v7a / armeabi\nDump : FULL DUMP\nOutil : CM2\n━━━━━━━━━━━━\n🔐 Mot de passe : MobiFirmware.VIP"},
    "dump_model_fne_nx9_official": {"en": "🔥 HONOR 70 — FNE-NX9 — Official Firmware 🔥\n━━━━━━━━━━━━\n💎 The official paid firmware — now available free of charge\n━━━━━━━━━━━━\n📦 Firmware details:\n• Model: HONOR 70 5G\n• Variant: FNE-NX9\n• Firmware: FNE-N29_def_meafnaf_8.0.0.292_C185E7R2P1\n• MagicOS: 8.0_0501AAEM\n• Hosting: Google Drive\n• Password: MobiFirmware.VIP\n━━━━━━━━━━━━\n📱 Specs:\n• 6.67 OLED 120Hz - Snapdragon 778G+ 5G\n• 8GB/12GB - 128/256/512GB\n• 54+50+2MP - 32MP - 4800mAh 66W\n━━━━━━━━━━━━\nHMAX-UNLOCKER - HithamMax", "fr": "🔥 HONOR 70 — FNE-NX9 — Firmware officiel 🔥\n━━━━━━━━━━━━\n💎 Le firmware officiel payant — désormais disponible gratuitement\n━━━━━━━━━━━━\n📦 Détails du firmware :\n• Modèle : HONOR 70 5G\n• Variante : FNE-NX9\n• Firmware : FNE-N29_def_meafnaf_8.0.0.292_C185E7R2P1\n• MagicOS : 8.0_0501AAEM\n• Hébergement : Google Drive\n• Mot de passe : MobiFirmware.VIP\n━━━━━━━━━━━━\n📱 Caractéristiques :\n• OLED 6,67 pouces 120 Hz - Snapdragon 778G+ 5G\n• 8 Go/12 Go - 128/256/512 Go\n• 54+50+2 MP - 32 MP - 4800 mAh 66 W\n━━━━━━━━━━━━\nHMAX-UNLOCKER - HithamMax"},
    "dump_model_hisorl_t901_full": {"en": "📱 NEW DUMP | HISORL T901 — FULL DUMP 🔥\n━━━━━━━━━━━━\nThe dump was pulled from a real device, prepared, and uploaded to Google Drive\nso that group members can use it when they need it.\n━━━━━━━━━━━━\n📱 Device: HISORL T901\n📁 Dump: Full Dump\n🔧 Tool: UnlockTool\n☁️ Storage: Google Drive\n🔐 Password: MobiFirmware.VIP\n━━━━━━━━━━━━\n🙏 Many thanks to our dear brother ĶĦălěď Ķäbô\nfor his effort in pulling this dump", "fr": "📱 NOUVEAU DUMP | HISORL T901 — FULL DUMP 🔥\n━━━━━━━━━━━━\nLe dump a été extrait d’un appareil réel, préparé et mis en ligne sur Google Drive\npour que les membres du groupe puissent l’utiliser en cas de besoin.\n━━━━━━━━━━━━\n📱 Appareil : HISORL T901\n📁 Dump : Full Dump\n🔧 Outil : UnlockTool\n☁️ Stockage : Google Drive\n🔐 Mot de passe : MobiFirmware.VIP\n━━━━━━━━━━━━\n🙏 Un grand merci à notre cher frère ĶĦălěď Ķäbô\npour son effort dans l’extraction de ce dump"},
    "dump_model_hmd_aura_ta1631": {"en": "📱 HMD AURA - TA-1631 - Official Firmware 📱\n━━━━━━━━━━━━\n📱 Device: HMD AURA\n🏷️ Model: TA-1631\n🔧 Codename: ROCKY - Unisoc SC9863A1 - Android 13\n📦 File: 2 Official Stock ROMs\n🏗️ Build 1: rck_116A-0-00WW-B01\n🏗️ Build 2: rck_1100-0-00WW-B01\n✅ 100% genuine, official and approved\n━━━━━━━━━━━━\n🛠️ Solves software problems such as:\n💀 Phone dead during a wrong flash\n⚠️ Software system problems\n🔧 Fixes boot, freezing and lag problems\n━━━━━━━━━━━━\n📱 Specs: 6.52 HD+ IPS - SC9863A1 - 2/3GB - 32GB - 5000mAh\n☁️ Upload: Google Drive - free direct link\n🔐 Pass: MobiFirmware.VIP", "fr": "📱 HMD AURA - TA-1631 - Firmwares officiels 📱\n━━━━━━━━━━━━\n📱 Appareil : HMD AURA\n🏷️ Modèle : TA-1631\n🔧 Nom de code : ROCKY - Unisoc SC9863A1 - Android 13\n📦 Fichier : 2 ROM stock officielles\n🏗️ Build 1 : rck_116A-0-00WW-B01\n🏗️ Build 2 : rck_1100-0-00WW-B01\n✅ 100 % originales, officielles et certifiées\n━━━━━━━━━━━━\n🛠️ Résout les problèmes logiciels tels que :\n💀 Téléphone mort lors d’un flashage incorrect\n⚠️ Problèmes du système logiciel\n🔧 Résout les problèmes de démarrage, de blocage et de lenteur\n━━━━━━━━━━━━\n📱 Caractéristiques : 6,52 HD+ IPS - SC9863A1 - 2/3 Go - 32 Go - 5000 mAh\n☁️ Hébergement : Google Drive - lien direct gratuit\n🔐 Mot de passe : MobiFirmware.VIP"},
    "dump_model_honor_50_lite_ntn_l22_new": {"en": "📱 Honor 50 Lite - NEW REGION C185 📱\n━━━━━━━━━━━━\n📱 Device: Honor 50 Lite\n🏷️ Model: NTN-L22 | C185\n🌍 Region routing: C185 - different routing - available to everyone\n🔧 Dump By: Unlock Tool\n✅ Status: read with Unlock Tool - ready to flash\n💡 It can be flashed with any tool that supports this type\n🎁 Free gift for technicians\n☁️ Upload: Google Drive\n━━━━━━━━━━━━\n🔐 Pass: MobiFirmware.VIP", "fr": "📱 Honor 50 Lite - NOUVELLE RÉGION C185 📱\n━━━━━━━━━━━━\n📱 Appareil : Honor 50 Lite\n🏷️ Modèle : NTN-L22 | C185\n🌍 Routage régional : C185 - routage différent - disponible pour tous\n🔧 Extrait avec : Unlock Tool\n✅ Statut : extrait avec Unlock Tool - prêt pour le flashage\n💡 Peut être flashé avec tout outil compatible avec ce type\n🎁 Cadeau gratuit pour les techniciens\n☁️ Téléversement : Google Drive\n━━━━━━━━━━━━\n🔐 Mot de passe : MobiFirmware.VIP"},
    "dump_model_honor_x7b_clk_lx2": {"en": "📱 Honor X7B - FULL DUMP 📱\n━━━━━━━━━━━━\n📱 Device: Honor X7B\n🏷️ Model: CLK-LX2 / C185\n📁 File: Full Dump\n🔧 Read By: UnlockTool\n☁️ Upload: Google Drive\n━━━━━━━━━━━━\n⚠️ Make sure the model, memory and board condition match before writing\n🔐 Pass: MobiFirmware.VIP", "fr": "📱 Honor X7B - FULL DUMP 📱\n━━━━━━━━━━━━\n📱 Appareil : Honor X7B\n🏷️ Modèle : CLK-LX2 / C185\n📁 Fichier : Full Dump\n🔧 Extrait avec : UnlockTool\n☁️ Téléversement : Google Drive\n━━━━━━━━━━━━\n⚠️ Vérifiez que le modèle, la mémoire et l’état de la carte correspondent avant l’écriture\n🔐 Mot de passe : MobiFirmware.VIP"},
    "dump_model_honor_x9c_full_dump": {"en": "⭐ HONOR X9c — FULL DUMP 🔥\nThe full dump was uploaded to Google Drive based on technicians' needs, to provide a ready-to-use file for software and programming work. 💛🔥\n━━━━━━━━━━━━━━━━━━\n📱 Phone specs:\n🔹 Model: HONOR X9c\n🔹 Processor: Qualcomm Snapdragon 6 Gen 1\n🔹 Display: 6.78\" AMOLED\n🔹 Resolution: 2700 × 1224 — 1.5K\n🔹 Refresh Rate: 120Hz\n🔹 Main Camera: 108MP + OIS\n🔹 Battery: 6600mAh\n🔹 Charging: 66W HONOR SuperCharge\n🔹 OS: MagicOS 8.0 — Android 14\n🔹 Network: 5G / 4G LTE\n━━━━━━━━━━━━━━━━━━\n📁 File details:\nDevice: HONOR X9c\nFile: FULL DUMP\nPulled By: Flash64 Ultra\nUpload: Google Drive\nPass File: MobiFirmware.VIP\n━━━━━━━━━━━━━━━━━━\nHMAX hithamMax - PROFESSIONAL FIRMWARE SOLUTIONS", "fr": "⭐ HONOR X9c — FULL DUMP 🔥\nLe dump complet a été mis en ligne sur Google Drive selon les besoins des techniciens, pour un fichier prêt à l’emploi pour les travaux logiciels et de programmation. 💛🔥\n━━━━━━━━━━━━━━━━━━\n📱 Caractéristiques du téléphone :\n🔹 Modèle : HONOR X9c\n🔹 Processeur : Qualcomm Snapdragon 6 Gen 1\n🔹 Écran : 6,78\" AMOLED\n🔹 Résolution : 2700 × 1224 — 1.5K\n🔹 Taux de rafraîchissement : 120 Hz\n🔹 Appareil photo principal : 108 MP + OIS\n🔹 Batterie : 6600 mAh\n🔹 Charge : 66 W HONOR SuperCharge\n🔹 Système : MagicOS 8.0 — Android 14\n🔹 Réseau : 5G / 4G LTE\n━━━━━━━━━━━━━━━━━━\n📁 Détails du fichier :\nAppareil : HONOR X9c\nFichier : FULL DUMP\nExtrait par : Flash64 Ultra\nTéléversement : Google Drive\nMot de passe : MobiFirmware.VIP\n━━━━━━━━━━━━━━━━━━\nHMAX hithamMax - SOLUTIONS FIRMWARE PROFESSIONNELLES"},
    "dump_model_itel_a06_a669w_full_dump_unlocktool": {"en": "🔥 iTEL A06 - A669W — FULL DUMP 🔥\n━━━━━━━━━━━━\n📱 Device name: iTEL A669W\n📱 Model number: A669W\n🔧 Firmware: A669W-SA375A-UGO-OP-250114V1604\n🔧 Full Dump — read with UnlockTool\n✍️ By Hamallah\n━━━━━━━━━━━━\n📋 Dump information\n📦 File type: Full Dump\n📦 File size: about 2.00 GB\n📦 File format: ZIP\n🔧 Read tool: UnlockTool\n🔧 Build: 250114\n🔧 Version: V1604\n━━━━━━━━━━━━\n👤 The dump was pulled by our brother, a group member\n🙏 Hamallah Abdelmalek\nMany thanks and appreciation for his contribution to helping technicians\n━━━━━━━━━━━━\n☁️ The dump was uploaded to Google Drive\n🔐 Pass File: MobiFirmware.VIP\n━━━━━━━━━━━━\n🔧 Full Dump | UnlockTool | ready for software and maintenance work\nHMAX hithamMax", "fr": "🔥 iTEL A06 - A669W — FULL DUMP 🔥\n━━━━━━━━━━━━\n📱 Nom de l’appareil : iTEL A669W\n📱 Numéro de modèle : A669W\n🔧 Firmware : A669W-SA375A-UGO-OP-250114V1604\n🔧 Full Dump — extrait avec UnlockTool\n✍️ Par Hamallah\n━━━━━━━━━━━━\n📋 Informations sur le dump\n📦 Type de fichier : Full Dump\n📦 Taille du fichier : environ 2,00 Go\n📦 Format du fichier : ZIP\n🔧 Outil d’extraction : UnlockTool\n🔧 Build : 250114\n🔧 Version : V1604\n━━━━━━━━━━━━\n👤 Le dump a été extrait par notre frère, membre du groupe\n🙏 Hamallah Abdelmalek\nMerci beaucoup pour sa contribution à l’aide des techniciens\n━━━━━━━━━━━━\n☁️ Le dump a été mis en ligne sur Google Drive\n🔐 Mot de passe : MobiFirmware.VIP\n━━━━━━━━━━━━\n🔧 Full Dump | UnlockTool | prêt pour les travaux logiciels et la maintenance\nHMAX hithamMax"},
    "dump_model_itel_l6503_vision2": {"en": "📱 Itel L6503 - Itel Vision 2 - 3 Dumps 📱\n━━━━━━━━━━━━\n🏷️ Model: L6503\n🔧 Chipset: Unisoc SC9863A Octa 1.6GHz IMG8322\n📦 RAM: 2GB/3GB - Storage: 32GB/64GB eMMC\n📱 Display: 6.6 HD+ 720x1600\n🔋 Battery: 5000mAh - Android 10 Go\n━━━━━━━━━━━━\n📦 Dump 1 - CM2:\n🔖 Build: L6503-F6315-10.0-OP-V049-20221213\n📦 Size: 3GB\n📦 Dump 2 - UnlockTool Full Dump:\n🔖 Build: L6503-F6315-10.0-OP-V049-20221213\n📦 Size: 1.7GB\n📦 Dump 3 - Pandora Tool:\n📦 Size: 1.7GB\n━━━━━━━━━━━━\n☁️ Upload: Google Drive - 3 links\n🔐 Pass: MobiFirmware.VIP\n🎯 Our goal: the technician finds what they need without wasting time", "fr": "📱 Itel L6503 - Itel Vision 2 - 3 Dumps 📱\n━━━━━━━━━━━━\n🏷️ Modèle : L6503\n🔧 Processeur : Unisoc SC9863A Octa 1,6 GHz IMG8322\n📦 RAM : 2 Go/3 Go - Stockage : 32 Go/64 Go eMMC\n📱 Écran : 6,6 HD+ 720x1600\n🔋 Batterie : 5000 mAh - Android 10 Go\n━━━━━━━━━━━━\n📦 Dump 1 - CM2 :\n🔖 Build : L6503-F6315-10.0-OP-V049-20221213\n📦 Taille : 3 Go\n📦 Dump 2 - UnlockTool Full Dump :\n🔖 Build : L6503-F6315-10.0-OP-V049-20221213\n📦 Taille : 1,7 Go\n📦 Dump 3 - Pandora Tool :\n📦 Taille : 1,7 Go\n━━━━━━━━━━━━\n☁️ Téléversement : Google Drive - 3 liens\n🔐 Mot de passe : MobiFirmware.VIP\n🎯 Notre objectif : que le technicien trouve ce dont il a besoin sans perdre de temps"},
    "dump_model_iphone16_pro_max_copy_mt6735": {"fr": "🍎 iPhone 16 Pro Max Copy - FULL DUMP 🍎\n━━━━━━━━━━━━\n📱 Appareil : iPhone 16 Pro Max Copy\n🏷️ Modèle : Pro_Max16 - dream2qltesq\n🔧 Plateforme : MT6735 - Build ID NRD90M\n📱 Système : Android 7.0 - SDK 24\n🛡️ Correctif : 2022-01-05\n🔖 Version FW : 1751029924\n📅 Date de build : 2025-06-27 21:19:38 CST\n📦 Type : FULL DUMP - Pandora Tool\n👤 Par : Prince Cazanova\n📦 Taille : 1,4 Go\n━━━━━━━━━━━━\n☁️ Google Drive\n🔐 Mot de passe : MobiFirmware.VIP"},
    "dump_model_huawei_y7a_ppa_lx2": {"fr": "📱 HUAWEI Y7A - FICHIER DUMP 📱\n━━━━━━━━━━━━\n📱 Appareil : HUAWEI Y7A\n🏷️ Modèle : PPA-LX2\n🔧 Extrait avec : EASY JTAG PLUS\n👨‍🔧 Téléversé par : Ing. Reynold Bermil Leonido\n☁️ Téléversement : Google Drive\n━━━━━━━━━━━━\n🔐 Mot de passe : MobiFirmware.VIP"},
    "dump_model_infinix_note_30_5g_x6711_v600": {"fr": "📱 INFINIX NOTE 30 5G - FULL DUMP 📱\n━━━━━━━━━━━━\n📱 Appareil : INFINIX NOTE 30 5G\n🏷️ Modèle : X6711 - V600\n📁 Fichier : FULL DUMP\n🔧 Extrait avec : Pandora Tool\n━━━━━━━━━━━━\n🔐 Mot de passe : MobiFirmware.VIP"},
    "dump_model_infinix_x657c_smart5": {"fr": "📱 Infinix Smart 5 - X657C - Full Dump + NV 📱\n━━━━━━━━━━━━\n🏷️ Modèle : X657C - Smart 5\n🔖 Firmware : X657C-H6117GH-QGo-GL-210825V252\n📦 Type : fichier Full Dump + fichier NV\n🔧 Outil : Unlock Tool\n📦 Taille : 1,6 Go\n━━━━━━━━━━━━\n📱 Caractéristiques : écran 6,6 IPS LCD 720x1600\n🔧 Helio A20 - RAM 2/3 Go - 32/64 Go\n📸 13 MP - 5000 mAh\n━━━━━━━━━━━━\n☁️ Google Drive\n🔐 Mot de passe : MobiFirmware.VIP"},
    "dump_model_itel_p37_p651w": {"fr": "🔥 ITEL P37 - P651W 🔥\n━━━━━━━━━━━━\n📱 Marque : ITEL\n📌 Modèle : P37\n🔧 Code : P651W\n🏗️ Build : F3116-10.0-OP-V70-2023022\n💾 Type : Unlock Tool Full Dump + fichier NV\n━━━━━━━━━━━━\n🔐 Mot de passe : MobiFirmware.VIP"},
    "dump_model_nokia_5_3_ta_1234": {"fr": "📱 NOKIA 5.3 - FULL DUMP 📱\n━━━━━━━━━━━━\n📱 Appareil : NOKIA 5.3\n🏷️ Modèle : TA-1234 00WW_2_290_SP02\n📁 Fichier : FULL DUMP\n🔧 Extrait avec : Pandora Tool\n☁️ Téléversement : Google Drive\n━━━━━━━━━━━━\n🔐 Mot de passe : MobiFirmware.VIP"},
    "dump_model_lake_poco_c75_14c_17c": {"en": "⭐ lake POCO C75 Redmi 14C REDMI 17C Redmi A3 Pro — 1 GB Dump 🔥\n━━━━━━━━━━━━\n🙏 Many thanks to our member Hossam Khairy\nfor sharing his dump with us\n━━━━━━━━━━━━\n📱 POCO C75: Helio G81 Ultra | 6.88\" IPS LCD 120Hz | 720×1640 HD+ | 50MP+AI | 5160mAh 18W | Android 14 HyperOS | 4G LTE\n📱 Redmi 14C: MediaTek Helio G81 Ultra | 6.88\" IPS LCD 120Hz | 720×1640 HD+ | 50MP+AI | 5160mAh 18W | Android 14 HyperOS\n📱 REDMI 17C: MediaTek Helio G85 | 6.7\" IPS LCD 90Hz | 720×1600 HD+ | 50MP+AI | 5000mAh 10W | Android 14 HyperOS\n📱 Redmi A3 Pro: MediaTek Helio G36 | 6.7\" IPS LCD 90Hz | 720×1600 HD+ | 8MP | 5000mAh 10W | Android 14 Go Edition\n━━━━━━━━━━━━\n📁 File details:\nDevice: POCO C75 / Redmi 14C / REDMI 17C / Redmi A3 Pro\nFile: 1GB DUMP (with network files)\nPulled By: Flash64 Ultra\nUpload: Google Drive\nPass File: MobiFirmware.VIP\n━━━━━━━━━━━━\nHMAX hithamMax - PROFESSIONAL FIRMWARE SOLUTIONS", "fr": "⭐ lake POCO C75 Redmi 14C REDMI 17C Redmi A3 Pro — Dump 1 Go 🔥\n━━━━━━━━━━━━\n🙏 Un grand merci à notre membre Hossam Khairy\npour avoir partagé son dump avec nous\n━━━━━━━━━━━━\n📱 POCO C75 : Helio G81 Ultra | écran 6,88\" IPS LCD 120 Hz | 720×1640 HD+ | 50 MP+IA | 5160 mAh 18 W | Android 14 HyperOS | 4G LTE\n📱 Redmi 14C : MediaTek Helio G81 Ultra | 6,88\" IPS LCD 120 Hz | 720×1640 HD+ | 50 MP+IA | 5160 mAh 18 W | Android 14 HyperOS\n📱 REDMI 17C : MediaTek Helio G85 | 6,7\" IPS LCD 90 Hz | 720×1600 HD+ | 50 MP+IA | 5000 mAh 10 W | Android 14 HyperOS\n📱 Redmi A3 Pro : MediaTek Helio G36 | 6,7\" IPS LCD 90 Hz | 720×1600 HD+ | 8 MP | 5000 mAh 10 W | Android 14 Go Edition\n━━━━━━━━━━━━\n📁 Détails du fichier :\nAppareil : POCO C75 / Redmi 14C / REDMI 17C / Redmi A3 Pro\nFichier : DUMP 1 Go (avec fichiers réseau)\nExtrait par : Flash64 Ultra\nTéléversement : Google Drive\nMot de passe : MobiFirmware.VIP\n━━━━━━━━━━━━\nHMAX hithamMax - SOLUTIONS FIRMWARE PROFESSIONNELLES"},
    "dump_model_m_horse_hot_30_full_dump_unlocktool": {"en": "🔥 M-HORSE HOT 30 — FULL DUMP 🔥\n🔧 BY UNLOCKTOOL | DUMPING-FIRMWARE\n━━━━━━━━━━━━\n📱 Device: M-HORSE HOT 30\n📱 Type: Full Dump\n🔧 Tool: UnlockTool\n📦 Version: HOT 30-M-HORSE-V05-20240410\n✍️ By Hamallah\n🔐 Pass: MobiFirmware.VIP\n━━━━━━━━━━━━\n⚠️ Warning: do NOT flash a different version - back up the network (NV) data first\n🙏 Thanks to our brother Hamallah Abdelmalek — Hamallah\nHMAX hithamMax", "fr": "🔥 M-HORSE HOT 30 — FULL DUMP 🔥\n🔧 EXTRAIT AVEC UNLOCKTOOL | DUMPING-FIRMWARE\n━━━━━━━━━━━━\n📱 Appareil : M-HORSE HOT 30\n📱 Type : Full Dump\n🔧 Outil : UnlockTool\n📦 Version : HOT 30-M-HORSE-V05-20240410\n✍️ Par Hamallah\n🔐 Mot de passe : MobiFirmware.VIP\n━━━━━━━━━━━━\n⚠️ Attention : ne flashez PAS une version différente - sauvegardez d’abord les données réseau (NV)\n🙏 Merci à notre frère Hamallah Abdelmalek — Hamallah\nHMAX hithamMax"},
    "dump_model_mhorse_c55_dual": {"en": "📱 M-Horse C55 - FULL DUMP DUAL TOOLS 📱\n━━━━━━━━━━━━\nNot just a dump... with more than one tool to solve the mismatch problem\n📱 Device: M-Horse C55\n🏷️ Version: C55-M-HORSE-V02-20240105\n🏭 Brand: DOOGEE X96Pro\n🖥️ Platform: sp9863a s9863a3h10\n📅 Build: 1/5/2024 - SW 11141\n💾 Size: 1.7 GB\n🔧 Dump: Pandora Tool + CM2 DUMP\n👨‍🔧 Thanks: Eng. Hossam Mostafa\n☁️ Upload: Google Drive\n━━━━━━━━━━━━\n🔐 Pass: MobiFirmware.VIP", "fr": "📱 M-Horse C55 - FULL DUMP DOUBLE OUTILS 📱\n━━━━━━━━━━━━\nPas seulement un dump... plusieurs outils pour résoudre le problème de non-correspondance\n📱 Appareil : M-Horse C55\n🏷️ Version : C55-M-HORSE-V02-20240105\n🏭 Marque : DOOGEE X96Pro\n🖥️ Plateforme : sp9863a s9863a3h10\n📅 Build : 1/5/2024 - SW 11141\n💾 Taille : 1,7 Go\n🔧 Dump : Pandora Tool + CM2 DUMP\n👨‍🔧 Remerciements : Ing. Hossam Mostafa\n☁️ Téléversement : Google Drive\n━━━━━━━━━━━━\n🔐 Mot de passe : MobiFirmware.VIP"},
    "dump_model_m_horse_spark_10_pro_full_dump_unlocktool": {"en": "🔥 M-HORSE-SPARK 10 Pro — FULL DUMP 🔥\n🔧 Full Dump | UnlockTool\n━━━━━━━━━━━━\nA year ago we shared two dumps for the\n📱 M-HORSE-SPARK 10 Pro\nToday we add a third, different version, from our brother:\n🙏 Hamallah Abdelmalek ❤️\n━━━━━━━━━━━━\n🔹 Version 1: SPARK 10 Pro M-HORSE-V02-20231027\n🔐 Pass: MobiFirmware.VIP\n━━━━━━━━━━━━\n🔹 Version 2: SPARK 10Pro-M-HORSE-V05-20240410\n🔐 Pass: MobiFirmware.VIP\n━━━━━━━━━━━━\n🔹 Version 3 — NEW DUMP: SPARK 10Pro-M-HORSE-V06-20240716\n✍️ Provided by Hamallah Abdelmalek\n🔐 Pass: MobiFirmware.VIP\n━━━━━━━━━━━━\n📋 File type: Full Dump | Tool: UnlockTool\nDevice: SPARK 10 Pro M-HORSE\nSeveral versions to cover different builds\n━━━━━━━━━━━━\n⚠️ Very important for technicians\nDo NOT flash a version different from the one on the phone: the device may lose its connection and not boot.\nCheck the phone's version, use the matching dump, and back up the network first.\n━━━━━━━━━━━━\n🙏 Thanks to every member who helps technicians\nHMAX hithamMax", "fr": "🔥 M-HORSE-SPARK 10 Pro — FULL DUMP 🔥\n🔧 Full Dump | UnlockTool\n━━━━━━━━━━━━\nIl y a un an, nous avons partagé deux dumps pour le\n📱 M-HORSE-SPARK 10 Pro\nAujourd’hui, un troisième dump, d’une autre version, offert par notre frère :\n🙏 Hamallah Abdelmalek ❤️\n━━━━━━━━━━━━\n🔹 Version 1 : SPARK 10 Pro M-HORSE-V02-20231027\n🔐 Mot de passe : MobiFirmware.VIP\n━━━━━━━━━━━━\n🔹 Version 2 : SPARK 10Pro-M-HORSE-V05-20240410\n🔐 Mot de passe : MobiFirmware.VIP\n━━━━━━━━━━━━\n🔹 Version 3 — NOUVEAU DUMP : SPARK 10Pro-M-HORSE-V06-20240716\n✍️ Fourni par Hamallah Abdelmalek\n🔐 Mot de passe : MobiFirmware.VIP\n━━━━━━━━━━━━\n📋 Type : Full Dump | Outil : UnlockTool\nPlusieurs versions disponibles\n━━━━━━━━━━━━\n⚠️ Très important pour les techniciens\nNe flashez PAS une autre version que celle du téléphone : risque de perte de connexion et de non-démarrage.\nVérifiez la version, utilisez le dump correspondant et sauvegardez d’abord les données réseau.\n━━━━━━━━━━━━\n🙏 Merci à chaque membre qui aide les techniciens\nHMAX hithamMax"},
    "dump_model_mhorse_hot40pro_v03": {"en": "🐎 M-HORSE HOT 40 Pro - Full Dump 🐎\n━━━━━━━━━━━━\n📱 Device: M-HORSE HOT 40 Pro\n🏷️ Version: HOT 40 Pro-M-HORSE-V03-20240807\n📦 Type: Full Dump - UnlockTool By Hamallah\n👤 By: Hamallah Abdulmalek\n━━━━━━━━━━━━\n⚠️ Warning: flashing a different version is forbidden - make sure of the version\n💾 Back up the network files first, then flash\n━━━━━━━━━━━━\n☁️ Google Drive\n🔐 Pass: MobiFirmware.VIP", "fr": "🐎 M-HORSE HOT 40 Pro - Full Dump 🐎\n━━━━━━━━━━━━\n📱 Appareil : M-HORSE HOT 40 Pro\n🏷️ Version : HOT 40 Pro-M-HORSE-V03-20240807\n📦 Type : Full Dump - UnlockTool, par Hamallah\n👤 Par : Hamallah Abdulmalek\n━━━━━━━━━━━━\n⚠️ Attention : il est interdit de flasher une version différente - vérifiez bien la version\n💾 Sauvegardez d’abord les fichiers réseau, puis flashez\n━━━━━━━━━━━━\n☁️ Google Drive\n🔐 Mot de passe : MobiFirmware.VIP"},
    "dump_model_moto_e13_xt2345_4_pandora_full_dump": {"en": "🔥 Moto E13 — XT2345-4 — FULL DUMP 🔥\n━━━━━━━━━━━━\n🔨 DUMP BY PND TOOL\nA tested and reliable Full Dump, provided for technicians.\n━━━━━━━━━━━━\n📦 Dump data:\n• Model: Moto E13\n• Model Number: XT2345-4\n• Tool: PND Tool\n• Status: tested and reliable ✅\n• Upload: Google Drive\n━━━━━━━━━━━━\n🔐 Password: MobiFirmware.VIP", "fr": "🔥 Moto E13 — XT2345-4 — FULL DUMP 🔥\n━━━━━━━━━━━━\n🔨 DUMP EXTRAIT AVEC PND TOOL\nUn Full Dump éprouvé et fiable, mis à disposition des techniciens.\n━━━━━━━━━━━━\n📦 Données du dump :\n• Modèle : Moto E13\n• Numéro de modèle : XT2345-4\n• Outil : PND Tool\n• Statut : éprouvé et fiable ✅\n• Téléversement : Google Drive\n━━━━━━━━━━━━\n🔐 Mot de passe : MobiFirmware.VIP"},
    "dump_model_nokia_c10_ta_1342": {"en": "📱 NOKIA C10 - FULL DUMP 📱\n━━━━━━━━━━━━\n📱 Device: Nokia C10\n🏷️ Model: TA-1342\n🖥️ CPU/Platform: SC7731E Unisoc Spreadtrum\n🔧 Dump By: Pandora Tool\n💡 Note: most Spreadtrum/Unisoc dumps today are Pandora - UnlockTool gets stuck, and Android Multi Tool causes network problems\n⭐ Trusted Tools: InfinityBox CM2 & Pandora Tool\n☁️ Upload: Google Drive\n━━━━━━━━━━━━\n🔐 Pass: MobiFirmware.VIP", "fr": "📱 NOKIA C10 - FULL DUMP 📱\n━━━━━━━━━━━━\n📱 Appareil : Nokia C10\n🏷️ Modèle : TA-1342\n🖥️ Processeur / plateforme : SC7731E Unisoc Spreadtrum\n🔧 Extrait avec : Pandora Tool\n💡 Remarque : la plupart des dumps Spreadtrum/Unisoc actuels sont Pandora - UnlockTool se bloque et Android Multi Tool pose des problèmes de réseau\n⭐ Outils fiables : InfinityBox CM2 et Pandora Tool\n☁️ Téléversement : Google Drive\n━━━━━━━━━━━━\n🔐 Mot de passe : MobiFirmware.VIP"},
    "dump_model_oppo_a55_cph2325_f71": {"en": "📱 OPPO A55 — CPH2325 — FULL DUMP 🔥\n━━━━━━━━━━━━\n⚠️ The story:\nA device was flashed with an old dump from the group...\nThe result? The phone died 💀\n━━━━━━━━━━━━\n👤 Tested by:\nMohamed Mahmoud (Sharqia)\n━━━━━━━━━━━━\n🔥 The original version on the device:\nCPH2325_11_F.75\n━━━━━━━━━━━━\n❌ The tested dump:\nOPPO_CPH2325_11_F.71_DUMP BY PANDORA TOOL\nResult: the phone died\n━━━━━━━━━━━━\n✅ The version that solved the problem:\nCPH2325_11_F.67 - Solved ✅\n━━━━━━━━━━━━\n📌 Conclusion and golden advice:\nBefore you start flashing, know the device's version well,\ntake the network files, and try to choose the same version\nor one as close to it as possible.\n━━━━━━━━━━━━\n📱 Device: OPPO A55 CPH2325\n📦 File: CPH2325 11 F.71 FULL DUMP\n🔧 Tool: PANDORA TOOL\n📦 Size: 4.7 GB\n☁️ Hosting: Google Drive\n🔐 Pass: MobiFirmware.VIP", "fr": "📱 OPPO A55 — CPH2325 — FULL DUMP 🔥\n━━━━━━━━━━━━\n⚠️ L’histoire :\nUn appareil a été flashé avec un ancien dump présent dans le groupe...\nRésultat ? Le téléphone est mort 💀\n━━━━━━━━━━━━\n👤 Testé par :\nMohamed Mahmoud (Sharqia)\n━━━━━━━━━━━━\n🔥 La version d’origine de l’appareil :\nCPH2325_11_F.75\n━━━━━━━━━━━━\n❌ Le dump testé :\nOPPO_CPH2325_11_F.71_DUMP BY PANDORA TOOL\nRésultat : le téléphone est mort\n━━━━━━━━━━━━\n✅ La version qui a résolu le problème :\nCPH2325_11_F.67 - Résolu ✅\n━━━━━━━━━━━━\n📌 Conclusion et conseil d’or :\nAvant de commencer le flashage, connaissez bien la version de l’appareil,\nsauvegardez les fichiers réseau et choisissez de préférence la même version\nou une version aussi proche que possible.\n━━━━━━━━━━━━\n📱 Appareil : OPPO A55 CPH2325\n📦 Fichier : CPH2325 11 F.71 FULL DUMP\n🔧 Outil : PANDORA TOOL\n📦 Taille : 4,7 Go\n☁️ Hébergement : Google Drive\n🔐 Mot de passe : MobiFirmware.VIP"},
    "dump_model_realme_c35_rmx3511_full_a55": {"en": "📱 Realme C35 - FULL DUMP A.55 📱\n━━━━━━━━━━━━\n📱 Device: Realme C35\n🏷️ Model: RMX3511\n🏗️ Build: A.55\n📦 File: FULL DUMP\n🔧 Read By: Pandora Tool\n📚 Library: DUMPING-FIRMWARE\n☁️ Upload: Google Drive\n━━━━━━━━━━━━\n⚠️ Important: make sure the model and version match before writing\n🔐 Pass: MobiFirmware.VIP", "fr": "📱 Realme C35 - FULL DUMP A.55 📱\n━━━━━━━━━━━━\n📱 Appareil : Realme C35\n🏷️ Modèle : RMX3511\n🏗️ Build : A.55\n📦 Fichier : FULL DUMP\n🔧 Extrait avec : Pandora Tool\n📚 Bibliothèque : DUMPING-FIRMWARE\n☁️ Téléversement : Google Drive\n━━━━━━━━━━━━\n⚠️ Important : vérifiez que le modèle et la version correspondent avant l’écriture\n🔐 Mot de passe : MobiFirmware.VIP"},
    "dump_model_realme_c35_rmx3511_xml": {"en": "📱 Realme C35 - DUMP XML 128GB 📱\n━━━━━━━━━━━━\n📱 Device: Realme C35\n🏷️ Model: RMX3511\n📦 File: DUMP XML - 128GB\n🔧 Read By: Easy JTAG Plus\n👤 At the request of: Thamer Zarouki\n📚 Library: DUMPING-FIRMWARE\n☁️ Upload: Google Drive\n━━━━━━━━━━━━\n🔐 Pass: MobiFirmware.VIP", "fr": "📱 Realme C35 - DUMP XML 128 Go 📱\n━━━━━━━━━━━━\n📱 Appareil : Realme C35\n🏷️ Modèle : RMX3511\n📦 Fichier : DUMP XML - 128 Go\n🔧 Extrait avec : Easy JTAG Plus\n👤 À la demande de : Thamer Zarouki\n📚 Bibliothèque : DUMPING-FIRMWARE\n☁️ Téléversement : Google Drive\n━━━━━━━━━━━━\n🔐 Mot de passe : MobiFirmware.VIP"},
    "dump_model_tab_a9_sm_x110": {"en": "📱 Samsung Galaxy Tab A9 - FULL DUMP 📱\n━━━━━━━━━━━━\n📱 Device: Samsung Galaxy Tab A9\n🏷️ Model: SM-X110\n🏗️ Build: X110XXS6CYI3\n📦 File: FULL DUMP\n🔧 Read By: UnlockTool\n📚 Library: DUMPING-FIRMWARE\n☁️ Upload: Google Drive\n━━━━━━━━━━━━\n⚠️ Important: make sure SM-X110 and X110XXS6CYI3 match before writing\n🔐 Pass: MobiFirmware.VIP", "fr": "📱 Samsung Galaxy Tab A9 - FULL DUMP 📱\n━━━━━━━━━━━━\n📱 Appareil : Samsung Galaxy Tab A9\n🏷️ Modèle : SM-X110\n🏗️ Build : X110XXS6CYI3\n📦 Fichier : FULL DUMP\n🔧 Extrait avec : UnlockTool\n📚 Bibliothèque : DUMPING-FIRMWARE\n☁️ Téléversement : Google Drive\n━━━━━━━━━━━━\n⚠️ Important : vérifiez que SM-X110 et X110XXS6CYI3 correspondent avant l’écriture\n🔐 Mot de passe : MobiFirmware.VIP"},
    "dump_model_redmi_note14_5g_beryl_xml": {"en": "📱 Redmi Note 14 5G — Beryl — XML FULL DUMP 🔥\n━━━━━━━━━━━━\nToday we offer the device's XML FULL DUMP, pulled with the heavyweight tool:\n🔧 Easy JTAG Plus\n━━━━━━━━━━━━\n📱 Device: Redmi Note 14 5G — Beryl\n📁 File type: XML FULL DUMP\n📦 Dump size: 6.5 GB\n☁️ Uploaded to: Google Drive\n🔐 Pass File: MobiFirmware.VIP\n━━━━━━━━━━━━\n💾 A 6.5 GB dump, prepared for technicians to handle\ndevice cases and flashing operations.", "fr": "📱 Redmi Note 14 5G — Beryl — XML FULL DUMP 🔥\n━━━━━━━━━━━━\nAujourd’hui, nous vous proposons le XML FULL DUMP de l’appareil, extrait avec l’outil de référence :\n🔧 Easy JTAG Plus\n━━━━━━━━━━━━\n📱 Appareil : Redmi Note 14 5G — Beryl\n📁 Type de fichier : XML FULL DUMP\n📦 Taille du dump : 6,5 Go\n☁️ Mis en ligne sur : Google Drive\n🔐 Mot de passe : MobiFirmware.VIP\n━━━━━━━━━━━━\n💾 Un dump de 6,5 Go, préparé pour que les techniciens puissent gérer\nles cas de l’appareil et les opérations de flashage."},
    "dump_model_realme_c67_copy_full_dump_pandora": {"en": "🔥 REALME C67 COPY — FULL DUMP 🔥\n━━━━━━━━━━━━\n🛠️ FULL DUMP | Pandora Tool\n👤 By Prince Cazanova\n📦 File Size: 1.1 GB\n☁️ Uploaded on Google Drive\n🔐 Password: MobiFirmware.VIP\n━━━━━━━━━━━━\n📋 Dump Information\nModel: C67\nDevice: C67\nBoard: k80hd_bsp_fwv_512m\nPlatform: MTK6580_8.1\nAndroid Version: 8.1.0\nBuild ID: O11019\nDisplay ID: O11019 test-keys\nSecurity Patch: 2024-03-11\nUserdata: F2FS\n━━━━━━━━━━━━\n⚠️ Important for technicians: before any flashing, take a full backup of the network files and important data, and make sure the version and board match the device to avoid any problems.\n━━━━━━━━━━━━\nHMAX hithamMax", "fr": "🔥 REALME C67 COPY — FULL DUMP 🔥\n━━━━━━━━━━━━\n🛠️ FULL DUMP | Pandora Tool\n👤 Par Prince Cazanova\n📦 Taille du fichier : 1,1 Go\n☁️ Mis en ligne sur Google Drive\n🔐 Mot de passe : MobiFirmware.VIP\n━━━━━━━━━━━━\n📋 Informations sur le dump\nModèle : C67\nAppareil : C67\nCarte : k80hd_bsp_fwv_512m\nPlateforme : MTK6580_8.1\nVersion Android : 8.1.0\nID de build : O11019\nID d’affichage : O11019 test-keys\nCorrectif de sécurité : 2024-03-11\nDonnées utilisateur : F2FS\n━━━━━━━━━━━━\n⚠️ Important pour les techniciens : avant tout flashage, faites une sauvegarde complète des fichiers réseau et des données importantes, et vérifiez que la version et la carte correspondent à l’appareil pour éviter tout problème.\n━━━━━━━━━━━━\nHMAX hithamMax"},
    "dump_model_tecno_spark_40_pro_km6": {"en": "📱 Tecno Spark 40 Pro - FULL DUMP Android 15 📱\n━━━━━━━━━━━━\n📱 Device: Tecno Spark 40 Pro\n🏷️ Model: KM6\n🤖 Android: Android 15 Full Dump\n🔧 Tool: AMT\n💾 Size: 9.5 GB\n👨‍🔧 Uploaded by: Eng. Abdessamad Sbai\n☁️ Upload: Google Drive\n━━━━━━━━━━━━\n⚠️ Important warning before flashing:\nWhen opening AMT, choose: Camon 40 Pro\nbecause Spark 40 Pro is not directly supported inside the tool\n⚠️ Warning: back up the network files\nto avoid Anti-Crack or loss of network\n━━━━━━━━━━━━\n🔐 Pass: MobiFirmware.VIP", "fr": "📱 Tecno Spark 40 Pro - FULL DUMP Android 15 📱\n━━━━━━━━━━━━\n📱 Appareil : Tecno Spark 40 Pro\n🏷️ Modèle : KM6\n🤖 Android : Full Dump Android 15\n🔧 Outil : AMT\n💾 Taille : 9,5 Go\n👨‍🔧 Téléversé par : Ing. Abdessamad Sbai\n☁️ Téléversement : Google Drive\n━━━━━━━━━━━━\n⚠️ Avertissement important avant le flashage :\nDans AMT, choisissez : Camon 40 Pro\ncar le Spark 40 Pro n’est pas directement pris en charge par l’outil\n⚠️ Attention : sauvegardez les fichiers réseau\npour éviter l’Anti-Crack ou la perte du réseau\n━━━━━━━━━━━━\n🔐 Mot de passe : MobiFirmware.VIP"},
    "dump_model_villaon_v20_full_dump_unlocktool": {"en": "🔥 VILLAON V20 — FULL DUMP 🔥\n━━━━━━━━━━━━\n📱 Device name: VILLAON V20\n📦 File type: Full Dump Firmware\n🔧 Firmware: W-V673-V01.57-11.0-GBL\n🔧 Full Dump — read with Unlock Tool\n✍️ By Hamallah\n━━━━━━━━━━━━\n👤 The dump was pulled by our brother, a group member\n🙏 Hamallah Abdelmalek\nMany thanks and appreciation for his contribution ❤️\n━━━━━━━━━━━━\n☁️ The dump was uploaded to Google Drive\n📥 To download\n🔐 Pass File: MobiFirmware.VIP\n━━━━━━━━━━━━\n🔧 Full Dump | read with Unlock Tool\nHMAX-UNLOCKER HithamMax", "fr": "🔥 VILLAON V20 — FULL DUMP 🔥\n━━━━━━━━━━━━\n📱 Nom de l’appareil : VILLAON V20\n📦 Type de fichier : Full Dump Firmware\n🔧 Firmware : W-V673-V01.57-11.0-GBL\n🔧 Full Dump — extrait avec Unlock Tool\n✍️ Par Hamallah\n━━━━━━━━━━━━\n👤 Le dump a été extrait par notre frère, membre du groupe\n🙏 Hamallah Abdelmalek\nMerci beaucoup pour sa contribution ❤️\n━━━━━━━━━━━━\n☁️ Le dump a été mis en ligne sur Google Drive\n📥 Pour télécharger\n🔐 Mot de passe : MobiFirmware.VIP\n━━━━━━━━━━━━\n🔧 Full Dump | extrait avec Unlock Tool\nHMAX-UNLOCKER HithamMax"},
    "dump_model_the_oteeto_tab_15_full_dump_cm2": {"en": "🔥 The Oteeto TAB 15 — FULL DUMP 🔥\n━━━━━━━━━━━━\n💎 A very rare file, one you will not easily find online.\n━━━━━━━━━━━━\n📦 What did we provide today?\n🔥 An original Full Dump pulled directly from the device\n🔧 The file was pulled using CM2\n👨‍🔧 A file made for technicians and software work\n☁️ Uploaded and prepared on Google Drive\n━━━━━━━━━━━━\n📱 Device:\nThe Oteeto TAB 15\n📦 File type:\nFULL DUMP\n🔧 Tool:\nCM2\n🔐 Password:\nMobiFirmware.VIP\n━━━━━━━━━━━━\n💡 Rare files that others may search for for hours...\nyou will find them ready here.\n━━━━━━━━━━━━\nHMAX-UNLOCKER HithamMax", "fr": "🔥 The Oteeto TAB 15 — FULL DUMP 🔥\n━━━━━━━━━━━━\n💎 Un fichier très rare, qu’on ne trouve pratiquement pas en ligne.\n━━━━━━━━━━━━\n📦 Qu’avons-nous proposé aujourd’hui ?\n🔥 Un Full Dump original extrait directement de l’appareil\n🔧 Fichier extrait avec CM2\n👨‍🔧 Fichier destiné aux techniciens et aux travaux logiciels\n☁️ Mis en ligne et préparé sur Google Drive\n━━━━━━━━━━━━\n📱 Appareil :\nThe Oteeto TAB 15\n📦 Type de fichier :\nFULL DUMP\n🔧 Outil :\nCM2\n🔐 Mot de passe :\nMobiFirmware.VIP\n━━━━━━━━━━━━\n💡 Les fichiers rares que d’autres cherchent pendant des heures…\nvous les trouvez prêts ici.\n━━━━━━━━━━━━\nHMAX-UNLOCKER HithamMax"},
    "dump_model_ytab_ultra_35_full_dump_cm2": {"en": "🔥 YTAB ULTRA 35 — FULL DUMP 🔥\n━━━━━━━━━━━━\n🌟 BY CM2 ONLY | By Prince Cazanova 🌟\n📱 Device: YTAB ULTRA 35\n🔧 Dump Tool: Infinity CM2MT2\n📦 Dump Size: 3 GB\n☁️ Uploaded on: Google Drive\n🔐 Pass: MobiFirmware.VIP\n━━━━━━━━━━━━\nBrand: Ytab | Model: ULTRA35\nBoard: k50sv1_64_bsp | Platform: mt6750\nAndroid: 10 | Patch: 2025-02-01\nBuild: 07.07.2025 | Display ID: M55P30DDR_BYC_ULTRA35_Ytab_V1.0_20250707\nCPU: arm64-v8a | Created: CM2MT2 v2.38d1 — 2026-07-08\n━━━━━━━━━━━━\n⚠️ Make sure the board matches before flashing\nHMAX hithamMax", "fr": "🔥 YTAB ULTRA 35 — FULL DUMP 🔥\n━━━━━━━━━━━━\n🌟 AVEC CM2 UNIQUEMENT | Par Prince Cazanova 🌟\n📱 Appareil : YTAB ULTRA 35\n🔧 Outil d’extraction : Infinity CM2MT2\n📦 Taille du dump : 3 Go\n☁️ Mis en ligne sur : Google Drive\n🔐 Mot de passe : MobiFirmware.VIP\n━━━━━━━━━━━━\nMarque : Ytab | Modèle : ULTRA35\nCarte : k50sv1_64_bsp | Plateforme : mt6750\nAndroid : 10 | Correctif : 2025-02-01\nBuild : 07.07.2025 | ID d’affichage : M55P30DDR_BYC_ULTRA35_Ytab_V1.0_20250707\nCPU : arm64-v8a | Créé : CM2MT2 v2.38d1 — 2026-07-08\n━━━━━━━━━━━━\n⚠️ Vérifiez la correspondance de la carte avant le flashage\nHMAX hithamMax"},
    "dump_model_wiko_t10_full_dump_unlocktool": {"en": "🔥 New dumps | WIKO T10 — FULL DUMP 🔥\n━━━━━━━━━━━━\n📱 Device name: WIKO T10\n📱 Model number: W-V673-01 / W-V673-02\n🔧 Firmware: W-V673-V01.57-11.0-GBL\n🔧 Full Dump — read with Unlock Tool\n✍️ By Hamallah\n━━━━━━━━━━━━\n📋 Device specs\n🖥️ Screen: 6.5-inch IPS LCD\n📐 Resolution: 720 × 1600\n🧠 Processor: MediaTek Helio A22 — MT6761\nCPU: quad-core 2.0GHz Cortex-A53\nGPU: PowerVR GE8300\n💾 RAM: 2GB\n💾 Storage: 64GB + microSD support up to 512GB\n📷 Rear camera: 13MP with AF\n📷 Front camera: 5MP\n🔋 Battery: 5000mAh\n🤖 OS: Android 11 Go Edition\n📏 Dimensions: 163.94 × 75.79 × 8.97 mm\n⚖️ Weight: about 192 g\n📡 Networks: 2G / 3G / 4G LTE\n🔗 Bluetooth 5.0 + Wi-Fi + GPS + FM\n━━━━━━━━━━━━\n👤 The dump was pulled by our brother, a group member\n🙏 Hamallah Abdelmalek\nMany thanks and appreciation for his contribution\n━━━━━━━━━━━━\n☁️ The dump was uploaded to Google Drive\n🔐 Pass File: MobiFirmware.VIP\n━━━━━━━━━━━━\nHMAX-UNLOCKER HithamMax", "fr": "🔥 Nouveaux dumps | WIKO T10 — FULL DUMP 🔥\n━━━━━━━━━━━━\n📱 Nom de l’appareil : WIKO T10\n📱 Numéro de modèle : W-V673-01 / W-V673-02\n🔧 Firmware : W-V673-V01.57-11.0-GBL\n🔧 Full Dump — extrait avec Unlock Tool\n✍️ Par Hamallah\n━━━━━━━━━━━━\n📋 Caractéristiques de l’appareil\n🖥️ Écran : 6,5 pouces IPS LCD\n📐 Résolution : 720 × 1600\n🧠 Processeur : MediaTek Helio A22 — MT6761\nCPU : quadricœur 2,0 GHz Cortex-A53\nGPU : PowerVR GE8300\n💾 RAM : 2 Go\n💾 Stockage : 64 Go + microSD jusqu’à 512 Go\n📷 Appareil photo arrière : 13 MP avec AF\n📷 Appareil photo avant : 5 MP\n🔋 Batterie : 5000 mAh\n🤖 Système : Android 11 Go Edition\n📏 Dimensions : 163,94 × 75,79 × 8,97 mm\n⚖️ Poids : environ 192 g\n📡 Réseaux : 2G / 3G / 4G LTE\n🔗 Bluetooth 5.0 + Wi-Fi + GPS + FM\n━━━━━━━━━━━━\n👤 Le dump a été extrait par notre frère, membre du groupe\n🙏 Hamallah Abdelmalek\nMerci beaucoup pour sa contribution\n━━━━━━━━━━━━\n☁️ Le dump a été mis en ligne sur Google Drive\n🔐 Mot de passe : MobiFirmware.VIP\n━━━━━━━━━━━━\nHMAX-UNLOCKER HithamMax"},
    "dump_model_x6511b_factory_signed": {"en": "🔥 Infinix Smart 6 — X6511B — Factory Signed 🔥\n━━━━━━━━━━━━\n💎 Firmware version:\nX6511B-F6318-11.0-OP-V127-20230810\n━━━━━━━━━━━━\n✅ Factory Signed Firmware\n• Verified • Official • Secure\n🔨 Factory firmware tested 100%\n━━━━━━━━━━━━\n🎁 This firmware is paid on all sites\n🎁 and is available now for free\n━━━━━━━━━━━━\n🔐 Firmware password: MobiFirmware.VIP\n☁️ Download via Google Drive\n━━━━━━━━━━━━\n📦 Phone specs:\n• 6.6 HD+ screen\n• Unisoc SC9863A Octa-Core processor\n• RAM: 2GB - 32GB storage\n• 8MP rear camera - 5MP front\n• 5000mAh battery - Android 11 Go\n• 4G LTE - rear fingerprint - Micro-USB\n━━━━━━━━━━━━\nHMAX-UNLOCKER - HithamMax", "fr": "🔥 Infinix Smart 6 — X6511B — Factory Signed 🔥\n━━━━━━━━━━━━\n💎 Version du firmware :\nX6511B-F6318-11.0-OP-V127-20230810\n━━━━━━━━━━━━\n✅ Firmware Factory Signed\n• Vérifié • Officiel • Sécurisé\n🔨 Firmware d’usine testé à 100 %\n━━━━━━━━━━━━\n🎁 Ce firmware est payant sur tous les sites\n🎁 et il est disponible gratuitement ici\n━━━━━━━━━━━━\n🔐 Mot de passe du firmware : MobiFirmware.VIP\n☁️ Téléchargement via Google Drive\n━━━━━━━━━━━━\n📦 Caractéristiques du téléphone :\n• Écran 6,6 HD+\n• Processeur Unisoc SC9863A Octa-Core\n• RAM : 2 Go - stockage 32 Go\n• Appareil photo arrière 8 MP - avant 5 MP\n• Batterie 5000 mAh - Android 11 Go\n• 4G LTE - empreinte arrière - Micro-USB\n━━━━━━━━━━━━\nHMAX-UNLOCKER - HithamMax"},
    "dump_model_x6840b_full_dump": {"en": "🔥 Smart 20 — X6840B — FULL DUMP 🔥\n━━━━━━━━━━━━\n📱 DEVICE INFO:\n• Model: Smart 20\n• Model No.: X6840B\n• Firmware: 16.1.0.150SP02\n• Build ID: OP001PF001AZ\n━━━━━━━━━━━━\n📂 FILE INFO:\n• File Type: FULL DUMP\n• Dump Status: READBACK FROM DEVICE\n• Dump Tool: UnlockTool\n• Purpose: Software Service / Flashing\n━━━━━━━━━━━━\n🔧 SERVICE NOTES:\n• Suitable for work on the same Model & Build\n• The dump was pulled using UnlockTool\n• Recommended as a reference for the exact same version\n━━━━━━━━━━━━\n⚠️ IMPORTANT - before flashing:\n• Take a full backup of the original device\n• Pull the Network / Calibration files and keep a copy\n• Make sure Model + Build match before starting\n━━━━━━━━━━━━\n🔐 Password: MobiFirmware.VIP\n☁️ Host: Google Drive\n━━━━━━━━━━━━\nHMAX-UNLOCKER - HithamMax", "fr": "🔥 Smart 20 — X6840B — FULL DUMP 🔥\n━━━━━━━━━━━━\n📱 INFOS APPAREIL :\n• Modèle : Smart 20\n• N° de modèle : X6840B\n• Firmware : 16.1.0.150SP02\n• Build ID : OP001PF001AZ\n━━━━━━━━━━━━\n📂 INFOS FICHIER :\n• Type de fichier : FULL DUMP\n• Statut du dump : LECTURE DEPUIS L’APPAREIL\n• Outil d’extraction : UnlockTool\n• Usage : service logiciel / flashage\n━━━━━━━━━━━━\n🔧 NOTES DE SERVICE :\n• Adapté aux travaux sur le même modèle et le même build\n• Le dump a été extrait avec UnlockTool\n• Recommandé comme référence pour la version exacte\n━━━━━━━━━━━━\n⚠️ IMPORTANT - avant le flashage :\n• Faites une sauvegarde complète de l’appareil d’origine\n• Extrayez les fichiers Network / Calibration et gardez une copie\n• Vérifiez la correspondance modèle + build avant de commencer\n━━━━━━━━━━━━\n🔐 Mot de passe : MobiFirmware.VIP\n☁️ Hébergement : Google Drive\n━━━━━━━━━━━━\nHMAX-UNLOCKER - HithamMax"},
    "dump_model_vivo_y15s_v2120_pd2140f_full_dump_unlocktool": {"en": "🔥 Vivo Y15s (V2120) – PD2140F | Full Dump BY UnlockTool 🔥\n━━━━━━━━━━━━\n📱 A while ago we uploaded a dump for the same phone:\n🖤 Vivo Y15s (V2120)\n🔧 Model: PD2140F\n📦 Version: PD2140F_EX_A_6.37.2\n🔧 Dump By: UnlockTool\n🔗 Link to the previous dump\n🔐 Pass File: MobiFirmware.VIP\n━━━━━━━━━━━━\n💥 Today we add a new dump for the same phone, in a different version:\n🖤 Vivo Y15s (V2120)\n🔧 Model: PD2140F\n📦 Version: PD2140F_EX_A_6.45.5 NEW\n🔧 Dump By: UnlockTool\n🔐 Pass File: MobiFirmware.VIP\n━━━━━━━━━━━━━\n❓ Why a second dump for the same phone? An important note:\nMany people may already work with the dump that exists in the group,\nbut we wanted to offer this version too and make it available,\nbecause differences in software versions are sometimes a key factor in a successful repair.\nBoth dumps, as explained above, were pulled with UnlockTool.\n━━━━━━━━━━━━\n⚠️ Very important before flashing:\nPlease pull and save the Network Files before you start the flashing process.\n━━━━━━━━━━━━\nHMAX-UNLOCKER HithamMax", "fr": "🔥 Vivo Y15s (V2120) – PD2140F | Full Dump UnlockTool 🔥\n━━━━━━━━━━━━\n📱 Il y a quelque temps, nous avons mis en ligne un dump de ce téléphone :\n🖤 Vivo Y15s (V2120)\n🔧 Modèle : PD2140F\n📦 Version : PD2140F_EX_A_6.37.2\n🔧 Extrait avec : UnlockTool\n🔗 Lien vers le dump précédent\n🔐 Mot de passe : MobiFirmware.VIP\n━━━━━━━━━━━━\n💥 Aujourd’hui, nouveau dump de ce téléphone, dans une autre version :\n🖤 Vivo Y15s (V2120)\n🔧 Modèle : PD2140F\n📦 Version : PD2140F_EX_A_6.45.5 NEW\n🔧 Extrait avec : UnlockTool\n🔐 Mot de passe : MobiFirmware.VIP\n━━━━━━━━━━━━━\n❓ Pourquoi un second dump ? Note importante :\nBeaucoup travaillent déjà avec le dump du groupe,\nmais nous voulions proposer aussi cette version,\ncar les différences de version logicielle sont parfois décisives pour réussir une réparation.\nLes deux dumps ont été extraits avec UnlockTool.\n━━━━━━━━━━━━\n⚠️ Très important avant le flashage :\nSauvegardez d’abord les fichiers réseau (Network Files) avant le flashage.\n━━━━━━━━━━━━\nHMAX-UNLOCKER HithamMax"},
    "dump_model_oppo_cph1933_a5_2020_full_dump_pandora": {"en": "🔥 OPPO CPH1933 (A5 2020) — FULL DUMP 🔥\n━━━━━━━━━━━━\n📱 Device: OPPO A5 2020\n📋 Model: CPH1933\n🔧 Dump Tool: Pandora Tool\n📦 Dump Size: 3 GB\n☁️ Uploaded on: Google Drive\n👤 At the request of member: Ahmed EL-Melwany\n🔐 Pass File: MobiFirmware.VIP\n━━━━━━━━━━━━\n📊 Dump data\nOEM PK HASH: 6E91B529AAD0307F1FC67310DAB1FF821EB7AA02FA5620157A9D20E124F4E0B84897B1389836216B4F2CB50D8DBB87B8\nCPU: SM6125 (Snapdragon 665)\nVendor: OPPO\nMSM HW ID: 0010A0E100510000\nSBL SW Ver: 00000001\nProduct Brand: qti\nManufacturer: QUALCOMM\nProduct Model: OPPO A5 2020\nProduct Name: qssi\nProduct Device: qssi\nProduct Board: trinket\nBoard Platform: trinket\nBuild ID: RKQ1.200903.002\nBuild Date: Sat Sep 3 22:41:12 CST 2022\nDisplay ID: CPH1933_11_F.01\nSecurity Patch: 2022-09-05\nVersion SDK: 30\nVersion Release: 11\nVersion Codename: REL\nFirmware Version: 1662212765538\nUserdata FS Type: EXT4\n━━━━━━━━━━━━\n⚠️ Before flashing: check the device data and version, then back up the network files first\n━━━━━━━━━━━━\nHMAX hithamMax", "fr": "🔥 OPPO CPH1933 (A5 2020) — FULL DUMP 🔥\n━━━━━━━━━━━━\n📱 Appareil : OPPO A5 2020\n📋 Modèle : CPH1933\n🔧 Outil : Pandora Tool\n📦 Taille du dump : 3 Go\n☁️ Hébergement : Google Drive\n👤 À la demande du membre : Ahmed EL-Melwany\n🔐 Mot de passe : MobiFirmware.VIP\n━━━━━━━━━━━━\n📊 Données du dump\nOEM PK HASH: 6E91B529AAD0307F1FC67310DAB1FF821EB7AA02FA5620157A9D20E124F4E0B84897B1389836216B4F2CB50D8DBB87B8\nCPU: SM6125 (Snapdragon 665)\nVendor: OPPO\nMSM HW ID: 0010A0E100510000\nSBL SW Ver: 00000001\nProduct Brand: qti\nManufacturer: QUALCOMM\nProduct Model: OPPO A5 2020\nProduct Name: qssi\nProduct Device: qssi\nProduct Board: trinket\nBoard Platform: trinket\nBuild ID: RKQ1.200903.002\nBuild Date: Sat Sep 3 22:41:12 CST 2022\nDisplay ID: CPH1933_11_F.01\nSecurity Patch: 2022-09-05\nVersion SDK: 30\nVersion Release: 11\nVersion Codename: REL\nFirmware Version: 1662212765538\nUserdata FS Type: EXT4\n━━━━━━━━━━━━\n⚠️ Avant le flashage : vérifiez les données et la version, puis sauvegardez les fichiers réseau\n━━━━━━━━━━━━\nHMAX hithamMax"},
    "dump_model_allcall_magic_60_exclusive": {"fr": "🔥📱 DUMP EXCLUSIF ALLCALL MAGIC 60\nVous ne le trouverez pas en ligne\n━━━━━━━━━━━━━━━━━━━━━━\n📌 Version du dump :\nEG_AOS14.0_28.05.2025\n━━━━━━━━━━━━━━━━━━━━━━\n🛠️ Extrait avec :\nPandora Tool\n━━━━━━━━━━━━━━━━━━━━━━\n❤️ Merci à l’ingénieur Abdullah Ghanem\npour ses efforts dans l’extraction et la mise en ligne du dump\n🌹 Qu’Allah lui accorde le meilleur\n━━━━━━━━━━━━━━━━━━━━━━\n☁️ Mis en ligne sur Google Drive\n🔐 Mot de passe : MobiFirmware.VIP\n━━━━━━━━━━━━━━━━━━━━━━\n📞 https://wa.me/message/A3KQWHSSERCFG1"},
    "dump_model_honor_400_abr_n03_osv15": {"fr": "⭐ HONOR 400 — ABR-N03 — FULL DUMP | OSv15 🔥\n━━━━━━━━━━━━\n📁 Firmware :\nHONOR 400 - ABR-N03 9.0.0.213(C69E5R1P1)\nOSv15 FULL DUMP\n━━━━━━━━━━━━\n⚡ Extrait par :\nF64 ULTRA\n━━━━━━━━━━━━\n📱 Appareil : HONOR 400 ABR-N03\n🔢 Version : 9.0.0.213(C69E5R1P1)\n🟡 Système : OSv15 - FULL DUMP\n🔧 Outil : F64 ULTRA\n☁️ Hébergement : Google Drive\n🔐 Mot de passe : MobiFirmware.VIP"},
    "dump_model_nokia_ta_1114_copy": {"fr": "⭐ NOKIA TA-1114 — VERSION COPY — FICHIER FLASH 🔥\n━━━━━━━━━━━━\n📱 Appareil : NOKIA TA-1114\n🔖 Version : VERSION COPY\n💾 Processeur : SPREADTRUM\n⚡ Extrait avec : Miracle Box\n📤 Téléversé par : Ahmed ClaSsic\n━━━━━━━━━━━━\n☁️ Hébergement : Google Drive\n✅ Statut : FICHIER FLASH PRÊT"},
    "dump_model_oppo_a31_cph2015_128gb": {"fr": "🔥 NOUVEAU DUMP DISPONIBLE 🔥\n━━━━━━━━━━━━\n📱 OPPO A31 — CPH2015\n💾 DUMP eMMC 128 Go\n🔧 Extrait avec EASY JTAG PLUS\n📦 Taille : 2,4 Go\n☁️ Téléversement sur Google Drive\n🔐 Mot de passe : MobiFirmware.VIP\n━━━━━━━━━━━━\n📋 Appareil : OPPO A31 CPH2015\nFichier : DUMP eMMC 128 Go\nExtrait par : EASY JTAG PLUS\nTéléversement : Google Drive\n━━━━━━━━━━━━\nHMAX hithamMax - SOLUTIONS FIRMWARE PROFESSIONNELLES"},
    "dump_model_oppo_a54_cph2239_dead_boot": {"fr": "📱 OPPO A54 - Réparation Dead Boot 📱\n━━━━━━━━━━━━\n📱 Appareil : OPPO A54\n🏷️ Modèle : CPH2239_11_C.33 [Réparation Dead Boot]\n🔧 Outil : Unlock Tool\n📦 Fichier : Full dump + fichier Nv\n☁️ Téléversement : Google Drive\n━━━━━━━━━━━━\n🔐 Mot de passe : MobiFirmware.VIP"},
    "dump_model_oppo_a57_cph2387": {"fr": "🔥 OPPO A57 CPH2387 FICHIER DUMP 🔥\n━━━━━━━━━━━━━━━━━━━━\n📱 Modèle : OPPO A57 CPH2387\n🛠️ Fichier dump extrait par : EASY JTAG PLUS\n👤 Téléversé par : Reynold Bermil Leonido\n🔐 Mot de passe : MobiFirmware.VIP\n📅 Téléversé : oct. 2025\n📂 Format : BIN • DUMP • FULL\n━━━━━━━━━━━━━━━━━━━━\n✅ Vérifié • Sûr • Prêt\n📞 https://wa.me/message/A3KQWHSSERCFG1"},
    "dump_model_oppo_a6_pro_5g_cph2781": {"fr": "📱 OPPO A6 PRO 5G - FICHIER DUMP 📱\n━━━━━━━━━━━━\n📱 Appareil : OPPO A6 PRO 5G\n🏷️ Modèle : CPH2781_11.A.31\n💾 Stockage : UFS 128 Go\n🔧 Extrait par : F64 BOX\n☁️ Téléversement : Google Drive\n━━━━━━━━━━━━\n🔐 Mot de passe : MobiFirmware.VIP"},
    "dump_model_oppo_reno_12f_4g_cph2687": {"fr": "📱 OPPO RENO 12F 4G - FICHIER DUMP 📱\n━━━━━━━━━━━━\n🏷️ Modèle : CPH2687\n🛠️ Dump extrait avec : F64 BOX\n📦 Type de dump : Full Flash / Userdata / Boot / Recovery\n🧠 Chipset : MediaTek Helio G99\n💾 Mémoire : 8 Go de RAM • 256 Go de stockage\n📏 Taille du dump : 8,52 Go\n📅 Date : 2024-06-12 18:42 UTC\n📁 Fichier : CPH2687_F64BOX_FullDump_20240612.zip\n━━━━━━━━━━━━\n🔐 Mot de passe : MobiFirmware.VIP"},
    "dump_model_realme_10_pro_5g_rmx3661": {"fr": "📱 REALME 10 PRO 5G - FICHIER DUMP 📱\n━━━━━━━━━━━━\n📱 Appareil : REALME 10 PRO 5G\n🏷️ Modèle : RMX3661\n💾 Stockage : 256 Go UFS\n🔧 Extrait par : F64 BOX\n━━━━━━━━━━━━\n🔐 Mot de passe : MobiFirmware.VIP"},
    "dump_model_realme_c15_rmx2180": {"fr": "🔥 REALME C15 RMX2180 - FULL DUMP 🔥\n━━━━━━━━━━━━━━━━━━━━━━\n📌 Version du dump : RMX2180_11_A.26\n🛠️ Extrait avec : Pandora Tool\n📏 Taille : 5,6 Go\n☁️ Google Drive\n🔐 Mot de passe : MobiFirmware.VIP\n━━━━━━━━━━━━━━━━━━━━━━\n📞 https://wa.me/message/A3KQWHSSERCFG1"},
    "dump_model_realme_c71_rmx5303": {"fr": "🔥 REALME C71 RMX5303 - FULL DUMP 🔥\n━━━━━━━━━━━━━━━━━━━━━━\n📌 Version du dump : export_15_C.09\n🛠️ Extrait avec : Pandora Tool\n📏 Taille : 7,4 Go\n☁️ Google Drive\n🔐 Mot de passe : MobiFirmware.VIP\n━━━━━━━━━━━━━━━━━━━━━━\n📞 https://wa.me/message/A3KQWHSSERCFG1"},
    "dump_model_realme_note_60x_rmx3938": {"fr": "🟡 REALME NOTE 60X - FICHIER DUMP 🟡\n━━━━━━━━━━━━\n📱 Appareil : Realme Note 60X\n🏷️ Modèle : RMX3938\n💾 Stockage : 64 Go eMMC\n🛡️ Correctif : 2025-10-01\n🔧 Extrait par : F64 BOX\n━━━━━━━━━━━━\n🔐 Mot de passe : MobiFirmware.VIP"},
    "dump_model_redmi_15c_poco_c85": {"fr": "🔥 DUMP XIAOMI REDMI 15C / POCO C85 🔥\n━━━━━━━━━━━━━━━━━━━━\n📱 Modèles : REDMI 15C | POCO C85\n💾 Stockage : 256 Go eMMC\n📂 Type de fichier : DUMP FILE\n━━━━━━━━━━━━━━━━━━━━\n📌 Version : AP3A.240905.015.A2 OS2.0.221.0.VBNMIXM\n🛠️ Extraction : F64 ULTRA\n📏 Taille : 7,4 Go\n━━━━━━━━━━━━━━━━━━━━\nTéléversé par : Reynold Bermil Leonido\n☁️ Google Drive\n🔐 Mot de passe : MobiFirmware.VIP\n━━━━━━━━━━━━━━━━━━━━\n📞 https://wa.me/message/A3KQWHSSERCFG1"},
    "dump_model_redmi_9c_m2006c3mg": {"fr": "🔥 XIAOMI REDMI 9C M2006C3MG - FICHIER DUMP 🔥\n━━━━━━━━━━━━━━━━━━━━\n📱 Modèle : XIAOMI REDMI 9C\n🔢 Numéro de modèle : M2006C3MG\n📂 Type de fichier : DUMP FILE\n━━━━━━━━━━━━━━━━━━━━\n💾 Infos du dump\n🛠️ Extrait avec : EASY JTAG PLUS\n📏 Taille du dump : 3 Go\n━━━━━━━━━━━━━━━━━━━━\nTéléversé par : Reynold Bermil Leonido\n☁️ Google Drive\n🔐 Mot de passe : MobiFirmware.VIP\n━━━━━━━━━━━━━━━━━━━━\n📞 https://wa.me/message/A3KQWHSSERCFG1"},
    "dump_model_redmi_a3_c61": {"fr": "🔥 XIAOMI REDMI A3 C61 FULL DUMP 🔥\n━━━━━━━━━━━━━━━━━━━━\n📱 Appareil : REDMI A3 C61\n💾 Stockage : 64 Go\n📂 Fichier : FULL DUMP\n━━━━━━━━━━━━━━━━━━━━\n💿 INFORMATIONS DU DUMP\n📌 Version : 16.V816.0.7.0.WGRMIXM\n🛠️ Extrait avec : F64 ULTRA\n📏 Taille : 3,6 Go\n━━━━━━━━━━━━━━━━━━━━\n☁️ Google Drive\n🔐 Mot de passe : MobiFirmware.VIP\n━━━━━━━━━━━━━━━━━━━━\n📞 https://wa.me/message/A3KQWHSSERCFG1"},
    "dump_model_redmi_a3x_missi_android16": {"fr": "📱 Xiaomi Redmi A3x - missi - Dump Android 16 📱\n━━━━━━━━━━━━\n🏷️ Produit : missi - Redmi A3x\n📦 Fichier : Full Dump - Android 16\n🔧 Outil : AMT Tool\n📦 Taille : 4,5 Go\n👤 Remerciements : Abdessamad Sbai\n━━━━━━━━━━━━\n📱 Caractéristiques : Unisoc T603 Octa 1,8 GHz PowerVR GE8322\n💾 RAM : 3/4 Go LPDDR4X - 64/128 Go eMMC 5.1\n📱 Écran : 6,71 HD+ 1650x720 90 Hz\n📸 8 MP / 5 MP - 5000 mAh 10 W USB-C\n🔧 Empreinte latérale - Double SIM + microSD\n📱 Système d’origine : Android 14\n━━━━━━━━━━━━\n☁️ Téléversement : Google Drive\n🔐 Mot de passe : MobiFirmware.VIP"},
    "dump_model_vivo_y03t_pd2360f": {"fr": "🔥 VIVO Y03T (PD2360F) FULL DUMP 🔥\n━━━━━━━━━━━━━━━━━━━━\n📱 Appareil : VIVO Y03T\n🔢 Modèle : PD2360F\n💾 Stockage : 64 Go eMMC\n📂 Fichier : DUMP FILE (RAR)\n📌 Version : PD2360F_EX_A_14.0.12.3.W20.V000L1\n📏 Taille du dump : 4,9 Go\n🛠️ Extrait avec : F64 ULTRA\n━━━━━━━━━━━━━━━━━━━━\n👤 Téléversé par : Reynold Bermil Leonido\n🏷️ Crédit : DUMPING-FIRMWARE\n☁️ Serveur de téléversement : Google Drive\n🔐 Mot de passe : MobiFirmware.VIP"},
    "dump_model_vivo_y21d_pd2510f": {"fr": "🔥 VIVO Y21D (PD2510F) FULL DUMP 🔥\n━━━━━━━━━━━━━━━━━━━━\n📱 Appareil : VIVO Y21D\n🔢 Modèle : PD2510F\n💾 Stockage : 256 Go UFS\n📂 Fichier : DUMP FILE (RAR)\n📏 Taille du dump : 8,2 Go\n🛠️ Extrait avec : F64 ULTRA\n━━━━━━━━━━━━━━━━━━━━\n👤 Téléversé par : Reynold Bermil Leonido\n🏷️ Crédit : DUMPING-FIRMWARE\n☁️ Serveur de téléversement : Google Drive\n🔐 Mot de passe : MobiFirmware.VIP"},
    "dump_model_vivo_y27_y36_5g_v2248_pd2279f_ex_a_15_2_10_2_w20": {"fr": "🔥 VIVO Y27 & Y36 5G — V2248 — FULL DUMP RARE 🔥\n━━━━━━━━━━━━\n📱 SÉRIE DUMP | VIVO\nModèle : VIVO Y27 & Y36 5G — V2248\nFirmware : PD2279F_EX_A_15.2.10.2.W20\n━━━━━━━━━━━━\n📋 Informations sur l’appareil :\n• Appareil : V2248\n• Nom : V2248\n• Fabricant : vivo\n• Marque : vivo\n• Modèle : V2248; 1; PD2279F_EX\n• Plateforme : MTK6833; mt6833; mt6631_6635; connac1x\n• Version : PD2279F_EX_A_15.2.10.2.W20\n• Firmware : Funtouch OS 15; PD2279F_EX_A_15.2.10.2.W20.V000L1\n• Date du firmware : Mon May 19 21:18:38 CST 2025\n• Incrémental : compiler250519211703; 15.2.10.2.W20; compiler250519212336\n• Android : 15\n• Correctif de sécurité : 2025-05-01\n• ABI : arm64-v8a\n• Carte : k6833v1_64_k510\n━━━━━━━━━━━━\n🛠️ OUTILS PRIS EN CHARGE ✅\n✅ EASYJTAG-PLUS\n✅ FLASH64 ULTRA\n✅ MIPI TESTER\n━━━━━━━━━━━━\n💾 Taille du dump :\n• Compressé : 7,3 Go\n• Extrait : 17 Go\n🔐 Mot de passe : MobiFirmware.VIP\n☁️ Hébergement : Google Drive\n━━━━━━━━━━━━\nHMAX-UNLOCKER - HithamMax"},
    "dump_a075f": {"en": "⚡ **FULL DUMP firmware for A075F (A075FXXU1AYG6)**\n━━━━━━━━━━━━━━━━━━\n📌 **Solution details:**\nA final fix for the A075F shutdown problem after flashing or when using scatter flashes.\n\n• A **full DUMP** file was uploaded to revive the device successfully.\n• **Flashing method:** flash using the **TSM** tool.\n━━━━━━━━━━━━━━━━━━", "fr": "⚡ **FIRMWARE DUMP COMPLET pour A075F (A075FXXU1AYG6)**\n━━━━━━━━━━━━━━━━━━\n📌 **Détails de la solution :**\nSolution définitive au problème d’extinction de l’A075F après le flashage ou lors de l’utilisation de flashs scatter.\n\n• Un fichier **DUMP complet** a été mis en ligne pour réanimer l’appareil avec succès.\n• **Méthode de flashage :** le flashage se fait avec l’outil **TSM**.\n━━━━━━━━━━━━━━━━━━"},
    "dump_a146u1": {"en": "🛠️ **Revival firmware for SAMSUNG SM-A146U1**\n━━━━━━━━━━━━━━━━━━\n📌 **Version and notes:**\n• **Version:** `A146U1UEUDEYF5`\n• **Date:** 25 July 2025\n• This firmware was tested personally and with our colleague Hisham Moharram.\n\n⚠️ **Important notice:** please pull the network files from the phone before starting the flashing process.\n━━━━━━━━━━━━━━━━━━", "fr": "🛠️ **Firmware de réanimation pour SAMSUNG SM-A146U1**\n━━━━━━━━━━━━━━━━━━\n📌 **Version et remarques :**\n• **Version :** `A146U1UEUDEYF5`\n• **Date :** 25 juillet 2025\n• Ce firmware a été testé personnellement et avec notre collègue Hisham Moharram.\n\n⚠️ **Avertissement important :** veuillez extraire les fichiers réseau du téléphone avant de commencer le flashage.\n━━━━━━━━━━━━━━━━━━"},
    "dump_kxd_a07_a12": {"en": "🔥 We offer two different versions of KXD A07\n━━━━━━━━━━━━\n🟢 DUMP 02\nKXD A07 — Android 12\n🔨 Dump By Pandora Tool\nA07_KXD_V1.03_oy_20230924\n• Build ID: SP1A.210812.016\n• Security Patch: 2022-11-05\n• Firmware: 230103\n• Platform: SP9863A\n• Userdata: F2FS\n💾 Size: 2.2 GB\n☁️ Google Drive — FREE\n━━━━━━━━━━━━\n⚠️ Please take note, dear technician\n📌 KXD A07 has more than one version.\nCheck the Build ID, Display ID and software version before flashing.\n━━━━━━━━━━━━\n🔐 Files password\nMobiFirmware.VIP\n━━━━━━━━━━━━\nAnd in the end…\nWe are not just collecting files.\nThe file we offer today may be the reason a device works again tomorrow.\n━━━━━━━━━━━━\nHMAX-UNLOCKER - HithamMax", "fr": "🔥 Nous proposons deux versions différentes du KXD A07\n━━━━━━━━━━━━\n🟢 DUMP 02\nKXD A07 — Android 12\n🔨 Extrait avec Pandora Tool\nA07_KXD_V1.03_oy_20230924\n• Build ID : SP1A.210812.016\n• Correctif de sécurité : 2022-11-05\n• Firmware : 230103\n• Plateforme : SP9863A\n• Userdata : F2FS\n💾 Taille : 2,2 Go\n☁️ Google Drive — GRATUIT\n━━━━━━━━━━━━\n⚠️ Attention, cher technicien\n📌 Le KXD A07 existe en plusieurs versions.\nVérifiez le Build ID, le Display ID et la version du logiciel avant le flashage.\n━━━━━━━━━━━━\n🔐 Mot de passe des fichiers\nMobiFirmware.VIP\n━━━━━━━━━━━━\nEt pour finir…\nNous ne nous contentons pas de collecter des fichiers.\nLe fichier que nous proposons aujourd’hui peut être la raison pour laquelle un appareil refonctionnera demain.\n━━━━━━━━━━━━\nHMAX-UNLOCKER - HithamMax"},
    "dump_kxd_a07_a13": {"en": "🔥 We offer two different versions of KXD A07\n━━━━━━━━━━━━\n🟣 DUMP 01\nKXD A07 — Android 13\n🔨 Dump By Pandora Tool\nA07_KXD_A13_V1.263_oy_20250423\n• Build ID: TP1A.220624.014\n• Security Patch: 2025-05-05\n• Firmware: 250411\n• Platform: SP9863A\n• Userdata: F2FS\n💾 Size: 3 GB\n☁️ Google Drive — FREE\n━━━━━━━━━━━━\n⚠️ Take note, dear technician: this point matters more than the dump itself.\n📌 KXD A07 has more than one version.\nA dump made for one A07 may not work on every A07.\nBefore you press Flash:\n Check the Build ID\n Check the Display ID\n Check the software version\n Make sure the dump matches your device's version exactly.\n Don't rely on the model name alone.\nChoosing a non-matching file can turn a small software issue into a bigger one, or kill the device.\n━━━━━━━━━━━━\n🔐 Files password\nMobiFirmware.VIP\n━━━━━━━━━━━━\nHMAX-UNLOCKER - HithamMax", "fr": "🔥 Nous proposons deux versions différentes du KXD A07\n━━━━━━━━━━━━\n🟣 DUMP 01\nKXD A07 — Android 13\n🔨 Extrait avec Pandora Tool\nA07_KXD_A13_V1.263_oy_20250423\n• Build ID : TP1A.220624.014\n• Correctif de sécurité : 2025-05-05\n• Firmware : 250411\n• Plateforme : SP9863A\n• Userdata : F2FS\n💾 Taille : 3 Go\n☁️ Google Drive — GRATUIT\n━━━━━━━━━━━━\n⚠️ Attention, cher technicien : ce point est plus important que le dump lui-même.\n📌 Le KXD A07 existe en plusieurs versions.\nUn dump prévu pour un A07 ne fonctionnera pas forcément sur tous les A07.\nAvant d’appuyer sur Flash :\n Vérifiez le Build ID\n Vérifiez le Display ID\n Vérifiez la version du logiciel\n Assurez-vous que le dump correspond exactement à la version de votre appareil.\n Ne vous fiez pas uniquement au nom du modèle.\nChoisir un fichier non compatible peut transformer un petit problème logiciel en problème plus grave, voire rendre l’appareil inutilisable.\n━━━━━━━━━━━━\n🔐 Mot de passe des fichiers\nMobiFirmware.VIP\n━━━━━━━━━━━━\nHMAX-UNLOCKER - HithamMax"},
    "dump_nokia_c12_ta1583_pandora": {"en": "🔥 FIRMWARE -  C12 | TA-1583\n00WW_1_54B_SP01 - DUMP BY PANDORA TOOL\n━━━━━━━━━━━━\nAfter we published a dump for the C12 - TA-1583\nthat was read with CM2, we decided to provide another copy\nread with Pandora Tool.\n🎯 Goal: provide two copies made with two different tools for the same device.\n━━━━━━━━━━━━\n📦 DUMP INFORMATION\n📱 Device: C12\n🔖 Model: TA-1583\n⚙️ Version: 00WW_1_54B_SP01\n🔨 Tool: Pandora Tool\n💾 File Size: 2 GB\n☁️ Host: Google Drive\n🔐 Password: MobiFirmware.VIP\n━━━━━━━━━━━━\n⚠️ IMPORTANT BEFORE FLASHING\n1️⃣ NETWORK BACKUP\n2️⃣ CHECK DEVICE DATA\n3️⃣ SLOT A / B - if it gets stuck on the logo, switch the SLOT\n━━━━━━━━━━━━\nHMAX-UNLOCKER - HithamMax", "fr": "🔥 FIRMWARE -  C12 | TA-1583\n00WW_1_54B_SP01 - DUMP PAR PANDORA TOOL\n━━━━━━━━━━━━\nAprès avoir publié un dump du C12 - TA-1583\nextrait avec CM2, nous avons décidé de proposer une autre copie\nextraite avec Pandora Tool.\n🎯 Objectif : proposer deux copies réalisées avec deux outils différents pour le même appareil.\n━━━━━━━━━━━━\n📦 INFORMATIONS DU DUMP\n📱 Appareil : C12\n🔖 Modèle : TA-1583\n⚙️ Version : 00WW_1_54B_SP01\n🔨 Outil : Pandora Tool\n💾 Taille du fichier : 2 Go\n☁️ Hébergement : Google Drive\n🔐 Mot de passe : MobiFirmware.VIP\n━━━━━━━━━━━━\n⚠️ IMPORTANT AVANT LE FLASHAGE\n1️⃣ SAUVEGARDE DU RÉSEAU\n2️⃣ VÉRIFIEZ LES DONNÉES DE L’APPAREIL\n3️⃣ SLOT A / B - s’il reste bloqué sur le logo, changez de SLOT\n━━━━━━━━━━━━\nHMAX-UNLOCKER - HithamMax"},
    "dump_nokia_g21": {"en": "📱 **DUMP FILE for NOKIA G21 TA-1418**\n━━━━━━━━━━━━━━━━━━\nA complete DUMP file read from a Nokia G21 (model TA-1418).\n\nYou can download it directly via Google Drive, or visit the original file page on the Halabtech website using the buttons below:\n━━━━━━━━━━━━━━━━━━", "fr": "📱 **FICHIER DUMP pour NOKIA G21 TA-1418**\n━━━━━━━━━━━━━━━━━━\nFichier DUMP complet extrait d’un Nokia G21 (modèle TA-1418).\n\nVous pouvez le télécharger directement via Google Drive, ou consulter la page du fichier original sur le site Halabtech à l’aide des boutons ci-dessous :\n━━━━━━━━━━━━━━━━━━"},
    "dump_nokia_ta1380": {"en": "🔥 Official, tested firmware to revive TA-1380 🔥\n📱  C1 2nd Edition – TA-1380\n━━━━━━━━━━━━\nIf your device suffers from:\n🔹 lag or severe slowdown\n🔹 stuck on the logo\n🔹 automatic restarts\n🔹 Dead Boot / sudden death\nthen this firmware may be the solution, God willing. ✅\n━━━━━━━━━━━━\n📦 Firmware information:\nFirmware: TA-1380_SP7731E_HMD_Global_NOKIA_C1_2nd_Edition_OSv11_RP1A.201005.001_IRU\nCPU: SPD7731E\nFirmware Type: Full Firmware / Dead Boot Repair\nSupported Tool: Pandora Tool\nStatus: official ROM, tested and reliable ✅\n━━━━━━━━━━━━\n🛠️ How it works in brief:\n1- Download the firmware file and extract it.\nYou will find:\nrom.json\nHMDSW_Irisumts-122H-0-00WW-B01_user-images.zip\n2- Extract the HMDSW...zip file.\n3- Move rom.json into the firmware folder.\n4- Open Pandora Tool and select the rom.json file.\n5- Choose Update Firmware and start flashing.\n━━━━━━━━━━━━\n⚠️ Important note about Slot A / Slot B:\nOn some devices the phone may be on Slot B before flashing, then after the operation it switches to Slot A, gets stuck on the logo, and shows an error message.\nThe fix is simple:\nConnect the device again, switch it to Slot B, then restart.\nGod willing, the device will work normally for you.\n━━━━━━━━━━━━\n📥 Free direct download\nHMAX-UNLOCKER - HithamMax", "fr": "🔥 Firmware officiel et testé pour réanimer le TA-1380 🔥\n📱  C1 2nd Edition – TA-1380\n━━━━━━━━━━━━\nSi votre appareil présente :\n🔹 des ralentissements ou une forte lenteur\n🔹 un blocage sur le logo\n🔹 des redémarrages automatiques\n🔹 un Dead Boot / une mort soudaine\nce firmware peut être la solution, si Dieu le veut. ✅\n━━━━━━━━━━━━\n📦 Informations sur le firmware :\nFirmware : TA-1380_SP7731E_HMD_Global_NOKIA_C1_2nd_Edition_OSv11_RP1A.201005.001_IRU\nCPU : SPD7731E\nType de firmware : Full Firmware / Réparation Dead Boot\nOutil compatible : Pandora Tool\nStatut : ROM officielle, testée et fiable ✅\n━━━━━━━━━━━━\n🛠️ Méthode en bref :\n1- Téléchargez le fichier du firmware et décompressez-le.\nVous trouverez :\nrom.json\nHMDSW_Irisumts-122H-0-00WW-B01_user-images.zip\n2- Décompressez le fichier HMDSW...zip.\n3- Placez rom.json dans le dossier du firmware.\n4- Ouvrez Pandora Tool et sélectionnez le fichier rom.json.\n5- Choisissez Update Firmware et lancez le flashage.\n━━━━━━━━━━━━\n⚠️ Remarque importante concernant Slot A / Slot B :\nSur certains appareils, le téléphone peut être sur le Slot B avant le flashage, puis passer sur le Slot A après l’opération, rester bloqué sur le logo et afficher un message d’erreur.\nLa solution est simple :\nReconnectez l’appareil, passez-le sur le Slot B, puis redémarrez.\nSi Dieu le veut, l’appareil fonctionnera normalement.\n━━━━━━━━━━━━\n📥 Téléchargement direct et gratuit\nHMAX-UNLOCKER - HithamMax"},
    "dump_nokia_c12_ta1583_cm2": {"fr": "📱 Les détails du dump Nokia C12 TA-1583 CM2 ne sont pas encore disponibles."},
    "dump_model_itel_a49_a661l": {
        "en": "🔥 Itel A661L - A49 (A58 Pro) 🔥\n━━━━━━━━━━━━\n📱 Model: A661L / A49 / A58 Pro\n🛠️ Dump by Pandora Tool\n🔑 Password: MobiFirmware.VIP\n💎 A rare dump for the Itel A49, not available elsewhere\n✅ Tested 100% on a working device\n⚠️ Back up network files before flashing\nGood luck to everyone\nHMAX-UNLOCKER",
        "fr": "🔥 Itel A661L - A49 (A58 Pro) 🔥\n━━━━━━━━━━━━\n📱 Modèle : A661L / A49 / A58 Pro\n🛠️ Dump extrait avec Pandora Tool\n🔑 Mot de passe : MobiFirmware.VIP\n💎 Un dump rare pour l’Itel A49, introuvable ailleurs\n✅ Testé à 100 % sur un appareil fonctionnel\n⚠️ Sauvegardez les fichiers réseau avant le flashage\nBonne chance à tous\nHMAX-UNLOCKER",
    },
    # <<CARD_TEXT_ENTRIES>>
}


def _dump_card_text(user_id, callback, text):
    """Return the caption of a DUMP model card in the user's language."""
    lang = hmaxi18n.get_language(user_id)
    if lang in ("en", "fr"):
        return _DUMP_CARD_TEXT.get(callback, {}).get(lang, text)
    return text


# Shared lines of the DUMP brand/section menus. Longer phrases come first so
# that "Official Firmware Library" is replaced before "Firmware Library".
_DUMP_MENU_LINES = {
    "fr": [
        ("Official Firmware Library", "Bibliothèque officielle de firmwares"),
        ("FULL DUMP Library", "Bibliothèque de dumps complets"),
        ("Full Dump Library", "Bibliothèque de dumps complets"),
        ("Firmware Library", "Bibliothèque de firmwares"),
        ("Official Stock ROMs", "ROMs officielles d’origine"),
        ("Google Drive - Direct Link", "Google Drive - lien direct"),
        ("One Company - All Models", "Une seule entreprise - tous les modèles"),
        ("Brand:", "Marque :"),
        ("Select model:", "Sélectionnez le modèle :"),
        ("اختر الموديل:", "Sélectionnez le modèle :"),
        ("وفرنا إصدارين مختلفين من KXD A07:", "Nous proposons deux versions différentes du KXD A07 :"),
        ("📥 التحميل مباشر ومجاني", "📥 Téléchargement direct et gratuit"),
        ("💾 *فل دامب كوبي*", "💾 *Dumps complets COPY*"),
        ("📱 ITEL DUMP", "📱 DUMP ITEL"),
    ],
    "en": [
        ("اختر الموديل:", "Select model:"),
        ("وفرنا إصدارين مختلفين من KXD A07:", "We offer two different versions of KXD A07:"),
        ("📥 التحميل مباشر ومجاني", "📥 Direct free download"),
        ("💾 *فل دامب كوبي*", "💾 *Full dump copy*"),
    ],
}


def _dump_localize(user_id, text):
    """Localize the shared lines of DUMP menus; ar keeps the original text."""
    lang = hmaxi18n.get_language(user_id)
    for source, target in _DUMP_MENU_LINES.get(lang, []):
        text = text.replace(source, target)
    return text


_DUMP_BUTTON_TEXT = {
    "📥 رابط التحميل - Google Drive": {
        "en": "📥 Download link - Google Drive",
        "fr": "📥 Lien de téléchargement - Google Drive",
    },
    "📥 التحميل مجانا - Google Drive": {
        "en": "📥 Free download - Google Drive",
        "fr": "📥 Téléchargement gratuit - Google Drive",
    },
}


def _dump_fr_label(text):
    """French wording for English DUMP button labels (Back / Download)."""
    text = re.sub(r"\bBack to\b", "Retour à", text)
    text = re.sub(r"\bBack\b", "Retour", text)
    return re.sub(r"\bDownload\b", "Télécharger", text)


def _dump_btn(user_id, text):
    """Button label for DUMP screens: en/fr translate, ar keeps the original."""
    lang = hmaxi18n.get_language(user_id)
    if lang == "fr":
        translated = _DUMP_BUTTON_TEXT.get(text, {}).get("fr")
        return translated or _dump_fr_label(text)
    if lang == "en":
        return _DUMP_BUTTON_TEXT.get(text, {}).get("en", text)
    return text


def _dump_back_label(user_id, original="🔙 Back"):
    """Back label for DUMP screens: French gets "Retour", other languages keep ``original``."""
    if hmaxi18n.get_language(user_id) == "fr":
        return original.replace("Back", "Retour")
    return original


def _dump_nav_label(kind, lang):
    """Previous/next labels for paged DUMP lists (ar keeps the original text)."""
    if kind == "prev":
        return {"en": "⬅️ Previous", "fr": "⬅️ Précédent"}.get(lang, "⬅️ السابق")
    return {"en": "➡️ Next", "fr": "➡️ Suivant"}.get(lang, "➡️ التالي")


def hmax_tecno_page_items(page, page_size=TECNO_PAGE_SIZE):
    """Return ``(page, total_pages, items)`` for one TECNO library page.

    The requested page is clamped to the valid range so stale buttons (for
    example a page that no longer exists after the catalogue changes) keep
    working instead of crashing the bot.
    """
    if page_size < 1:
        raise ValueError("page_size must be positive")
    items = list(TECNO_DUMPS.items())
    total_pages = max(1, (len(items) + page_size - 1) // page_size)
    try:
        page = int(page)
    except (TypeError, ValueError):
        page = 1
    page = max(1, min(page, total_pages))
    start = (page - 1) * page_size
    return page, total_pages, items[start:start + page_size]


def hmax_tecno_page_for_model(model_key, page_size=TECNO_PAGE_SIZE):
    """Return the 1-based page holding ``model_key`` (page 1 when unknown).

    Used by the dump cards so the back button returns to the page the user
    came from instead of always jumping to the first page.
    """
    keys = list(TECNO_DUMPS.keys())
    if model_key not in keys:
        return 1
    return keys.index(model_key) // page_size + 1


def hmax_tecno_page_text(page, total_pages, lang="ar"):
    """Header text displayed above every page of the TECNO library."""
    if lang == "en":
        return (
            "📱 **TECNO - 141 Models - Full Library**\n"
            "☁️ Google Drive\n"
            "🔓 No password\n"
            "⚡ Latest firmware for every model\n"
            "📦 Ready to download\n"
            "\n"
            f"📄 Page {page} / {total_pages} • up to {TECNO_PAGE_SIZE} models per page"
        )
    if lang == "fr":
        return (
            "📱 **TECNO - 141 modèles - Bibliothèque complète**\n"
            "☁️ Google Drive\n"
            "🔓 Sans mot de passe\n"
            "⚡ Dernier firmware pour chaque modèle\n"
            "📦 Prêt à télécharger\n"
            "\n"
            f"📄 Page {page} / {total_pages} • jusqu’à {TECNO_PAGE_SIZE} modèles par page"
        )
    return (
        "📱 **TECNO - 141 Model - مكتبة كاملة**\n"
        "☁️ Google Drive\n"
        "🔓 بدون باسورد\n"
        "⚡ أحدث فلاشة لكل موديل\n"
        "📦 جاهزة للتحميل\n"
        "\n"
        f"📄 صفحة {page} / {total_pages} • حتى {TECNO_PAGE_SIZE} موديل في الصفحة"
    )


BANNED_FILE = "banned_users.txt"
BANNED_USERS = hmaxruntime.BannedUserCache(BANNED_FILE)
_SUBSCRIPTION_CACHE = hmaxruntime.TTLCache(ttl_seconds=15, max_entries=10000)
_BROADCAST_LOCK = threading.Lock()

TSM_EDITION_DESCRIPTION = (
    "✨ **TSM PRO EDITION 2026.10.16 | Update**\n"
    "━━━━━━━━━━━━━━━━━━\n\n"
    "**Added Nothing 4B Support [EDL Mode]**\n\n"
    "**Added Unisoc ADL Mode [Unknown USB Mode] [ZTE Devices]**\n"
    "• Remove FRP\n• Factory reset\n"
    "**Tested ZTE models:**\n"
    "• ZTE nubia Neo 2 5G [Z2352N]\n• ZTE Blade A56 [Z2473]\n"
    "• ZTE nubia V80 Pro [Z2576]\n• ZTE Blade A36 [Z2472]\n"
    "• ZTE nubia Neo 3 GT 5G [Z2465N]\n• ZTE Blade A55 [Z2450]\n"
    "• ZTE Blade A75 4G [Z2359]\n"
    "⚠️ **Note:** Method covers ZTE devices.\n\n"
    "**Added New Bits Samsung 2026 [EDL Mode]**\n"
    "• Remove FRP\n• Factory Reset\n• Read/Write Firmware/Dump\n\n"
    "**Supported Samsung models:**\n"
    "• Galaxy A23 5G [SM-A236B bitH]\n• Galaxy A23 5G [SM-A236E bitH]\n"
    "• Galaxy A23 5G [SM-A236M bitH]\n• Galaxy F14 4G [SM-E145F bitD]\n"
    "• Galaxy Z Flip4 [SM-F721N bit8]\n• Galaxy Z Fold3 5G [SM-F926N bitE]\n"
    "• Galaxy Z Fold6 [SM-F956N bit4]\n• Galaxy S21 FE 5G [SM-G990B2 bitK]\n"
    "• Galaxy Tab A9+ 5G [SM-X216C bitC]\n• Galaxy Tab A9+ 5G [SM-X216N bitD]\n\n"
    "**Added More Support:**\n"
    "• TCL 9185W\n• TCL T513Z\n• TCL 30+ [T676K]\n• ZTE NUBIA NEO 5G [8150N]\n"
    "• ZTE BLADE A112 [P635A60]\n• REDMAGIC 11S Pro [NX809J]\n"
    "• REDMAGIC Nova Gaming Table [NP03J]\n• honor play 20a\n"
    "• lenovo Tab M11 [TB330XU]\n• OUKITEL C68\n\n"
    "**Improved:** Fastboot Flasher for Moto/Xiaomi\n\n"
    "**Fixed bugs:**\n"
    "• Preloader Mode: Redmi A3 [blue], Poco C61 [blue], Poco C50 [blue]\n"
    "• Crash with Remove FRP MTP OS16\n• Change CSC\n"
    "• Select Moto Maps flashfile*/servicefile*\n\n"
    "━━━━━━━━━━━━━━━━━━\n"
    "📥 Download the TSM Pro Edition update using the button below:"
)
def _broadcast_worker_guard(worker, worker_args):
    try:
        worker(*worker_args)
    finally:
        _BROADCAST_LOCK.release()


def _start_broadcast_worker(worker, worker_args, admin_id):
    """Run only one user-facing broadcast at a time to protect Telegram rate limits."""
    if not _BROADCAST_LOCK.acquire(blocking=False):
        try:
            bot.send_message(admin_id, "⚠️ يوجد بث جارٍ الآن. انتظر حتى ينتهي ثم أعد المحاولة.")
        except Exception:
            pass
        return False

    try:
        Thread(
            target=_broadcast_worker_guard,
            args=(worker, worker_args),
            daemon=True,
        ).start()
    except Exception:
        _BROADCAST_LOCK.release()
        raise
    return True


def get_banned_users():
    """جلب قائمة آيديهات المحظورين من الذاكرة مع تحميل الملف مرة واحدة."""
    return BANNED_USERS.ids()


def get_all_banned_users():
    """جمع المحظورين الدائمين من Firebase مع القائمة المحلية للأدمن فقط."""
    banned = get_banned_users()
    if not db:
        return banned
    try:
        for page in hmaxruntime.iter_document_pages(db.collection("users")):
            for doc in page:
                data = doc.to_dict() or {}
                if data.get("is_banned", 0) == 1:
                    banned.add(str(data.get("id") or doc.id))
    except Exception as e:
        print(f"تعذر تحميل قائمة الحظر من Firebase: {e}")
    return banned


def ban_user_id(user_id):
    """حظر المستخدم محلياً وفي Firebase، مع اعتبار سجل التدقيق إضافياً."""
    uid = str(user_id)
    try:
        BANNED_USERS.update_local(uid, True)
    except Exception as e:
        print(f"تعذر تحديث قائمة الحظر المحلية للمستخدم {uid}: {e}")
        return False

    if not globals().get("db"):
        return True

    try:
        user_ref = globals()["db"].collection("users").document(uid)
        user_ref.set({"is_banned": 1}, merge=True)
        BANNED_USERS.set_status(uid, True)
    except Exception as e:
        BANNED_USERS.set_status(uid, True)
        print(f"⚠️ تعذر حفظ الحظر في Firebase للمستخدم {uid}: {e}")
        return False

    try:
        globals()["db"].collection("ban_logs").add({
            "user_id": int(uid),
            "action": "ban",
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        })
    except Exception as log_error:
        print(f"تعذر تسجيل عملية الحظر للمستخدم {uid}: {log_error}")
    return True


def unban_user_id(user_id):
    """فك الحظر بعد حفظ الحالة في Firebase، مع التراجع محلياً عند الفشل."""
    uid = str(user_id)
    try:
        BANNED_USERS.update_local(uid, False)
    except Exception as e:
        print(f"تعذر تحديث قائمة الحظر المحلية للمستخدم {uid}: {e}")
        return False

    try:
        if globals().get("db"):
            user_ref = globals()["db"].collection("users").document(uid)
            user_ref.set({"is_banned": 0}, merge=True)
            BANNED_USERS.set_status(uid, False)
            try:
                globals()["db"].collection("ban_logs").add({
                    "user_id": int(uid),
                    "action": "unban",
                    "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                })
            except Exception as log_error:
                print(f"تعذر تسجيل عملية فك الحظر للمستخدم {uid}: {log_error}")
        else:
            BANNED_USERS.set_status(uid, False)
        return True
    except Exception as e:
        # Keep the user blocked if the durable unban did not succeed.
        try:
            BANNED_USERS.update_local(uid, True)
        except Exception:
            BANNED_USERS.set_status(uid, True)
        print(f"⚠️ تعذر تسجيل فك الحظر في Firebase للمستخدم {uid}: {e}")
        return False


# ================= 1. الإعدادات =================
TOKEN = os.getenv("BOT_TOKEN", "").strip()
MY_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID", 560330933))
PORT = int(os.getenv("PORT", 10000))
CHANNEL_ID = "@haithamMax1"
CHANNEL_URL = "https://t.me/haithamMax1"
MY_CHANNEL_ID = "@haithamMax1"
WHATSAPP_URL = "https://wa.me/967772773388"
TELEGRAM_ADMIN = "https://t.me/hithamMax"
WHATSAPP_CHANNEL_1 = "https://whatsapp.com/channel/0029VbB8JX00gcfD5Y5o1G46"
WHATSAPP_CHANNEL_2 = "https://whatsapp.com/channel/0029Vb6TvYnA2pLEgTFZ5S1W"
INVITE_POINTS = 10

# ================= 🆕 نظام تصنيف المستخدمين =================
USER_RANKS = {
    0:    ("⚪ عضو جديد",     "newbie"),
    50:   ("🟢 عضو نشط",      "active"),
    150:  ("🔵 عضو متميز",    "distinguished"),
    300:  ("🟡 عضو ذهبي",     "gold"),
    600:  ("🟣 عضو بلاتيني",  "platinum"),
    1200: ("👑 VIP ملكي",     "vip"),
}

# 🆕 نقاط الإجراءات
POINTS_PER_ACTION = {
    "tool_click":   2,
    "request":      5,
    "daily_visit": 10,
    "invite":      INVITE_POINTS,
}
def iter_active_user_ids():
    """Yield eligible user IDs from Firestore in bounded cursor pages."""
    if not db:
        return
    for page in hmaxruntime.iter_document_pages(db.collection("users"), page_size=200):
        for doc in page:
            data = doc.to_dict() or {}
            banned_value = data.get("is_banned", 0)
            if banned_value is True or str(banned_value).strip() == "1":
                continue
            if not data.get("is_subscribed", True):
                continue
            uid = data.get("id") or doc.id
            if str(uid).isdigit():
                yield int(uid)


def broadcast_update_to_users():
    try:
        update_doc = db.collection("settings").document("latest_update").get()
        if not update_doc.exists:
            return "⚠️ لا يوجد أي تحديث مكتوب في قاعدة البيانات لنشره!"

        update_text = (update_doc.to_dict() or {}).get("text", "")
        if not update_text:
            return "⚠️ نص التحديث فارغ!"

        full_message = f"📢 **تحديث جديد في البوت!**\n\n{update_text}"
        channel_sent = False
        try:
            bot.send_message(chat_id=MY_CHANNEL_ID, text=full_message, parse_mode="Markdown")
            channel_sent = True
        except Exception as channel_error:
            print(f"خطأ في القناة: {channel_error}")

        success_count = 0
        failed_count = 0
        for uid in iter_active_user_ids():
            try:
                bot.send_message(chat_id=uid, text=full_message, parse_mode="Markdown")
                success_count += 1
            except Exception as send_error:
                failed_count += 1
                print(f"تعذر إرسال التحديث للمستخدم {uid}: {send_error}")
            time.sleep(0.05)

        report = f"✅ تم إرسال التحديث إلى {success_count} مستخدم."
        if failed_count:
            report += f"\n⚠️ تعذر الإرسال إلى {failed_count} مستخدم."
        if channel_sent:
            report += f"\n📢 تم النشر في القناة {MY_CHANNEL_ID}."
        else:
            report += "\n❌ فشل النشر في القناة (تأكد أن البوت مشرف)."
        return report
    except Exception as e:
        return f"❌ حدث خطأ أثناء البث: {e}"


def _broadcast_update_with_status(chat_id, status_message_id):
    report = broadcast_update_to_users()
    try:
        bot.edit_message_text(
            text=report,
            chat_id=chat_id,
            message_id=status_message_id,
            parse_mode="Markdown",
        )
    except Exception:
        bot.send_message(chat_id, report, parse_mode="Markdown")


def get_rank(points):
    """إرجاع (اسم_الرتبة, مفتاح_الرتبة) حسب النقاط"""
    rank_name = "⚪ عضو جديد"
    rank_key = "newbie"
    for threshold in sorted(USER_RANKS.keys(), reverse=True):
        if points >= threshold:
            rank_name, rank_key = USER_RANKS[threshold]
            break
    return rank_name, rank_key

def get_next_rank_info(points):
    """إرجاع معلومات الرتبة التالية"""
    for threshold in sorted(USER_RANKS.keys()):
        if points < threshold:
            return threshold, USER_RANKS[threshold][0]
    return None, None

# ================= 2. تهيئة Firebase =================
try:
    firebase_config = json.loads(os.getenv("FIREBASE_JSON_CONTENT", "{}"))
    cred = credentials.Certificate(firebase_config)
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("✅ Firebase Connected Successfully!")
except Exception as e:
    print(f"❌ Firebase Error: {e}")
    db = None

bot = telebot.TeleBot(TOKEN)
hmaxi18n.install(bot, db)

# ================= بيانات فتح شفرة الآيفون =================
IPHONE_UNLOCK_CODES_DESC = """**📟 الأكواد مقابلها اسم الشركة:**

USA AT&T 3104101 - 3131300 - 3104108
USA Verizon 2040400 or 3114806
USA Sprint(CDMA) 3160101 or 3160100 or 3102605 or 3101200 or 3101202
USA Cable&Wireless Lime 3461401
USA Sprint iPhone5 3101200
USA Cricket 2040400 - 3101508 or 3101500 - 3100901 - 3101507
USA Virgin iPhone5 3101200 - 3160101
USA Straight Talk 2040400
USA T-Mobile iPhone5 3102605
USA Wireless Alaska 3113700
USA T-Mobile 3102620 - 3102602
USA Tracfone 3114801
USA MetroPCS 3102600
USA Total Wireless 3114801
USA Consumer Cellular 3104101 - 3102620
USA Boost Mobile 3160101 - 3160100
USA Xfinity 2040400 - 2040438
US Cellular 3115801
US Virgin 3160101 - 3101200"""

IPHONE_METHOD_1_LINK = "https://www.mediafire.com/file/78yrp0yui10rme1/%25D8%25B4%25D8%25B1%25D9%258A%25D8%25AD%25D9%2587_%25D8%25A5%25D9%2584%25D9%2583%25D8%25AA%25D8%25B1%25D9%2588%25D9%2586%25D9%258A_%25D9%2584%25D9%2584%25D8%25A7%25D9%258A%25D9%2581%25D9%2588%25D9%2586_%25D8%25AB%25D8%25A8%25D8%25A7%25D8%25AA_%25D8%25A7%25D9%2584%25D8%25AA%25D8%25BA%25D8%25B7%25D9%258A%25D9%2587.txt/file"
IPHONE_METHOD_2_LINK = "https://www.mediafire.com/file/rno5wdrghobbsoo/%25D8%25A7%25D9%2584%25D8%25B7%25D8%25B1%25D9%258A%25D9%2582%D9%87_%25D8%25A7%25D9%2584%D8%AB%D8%A7%D9%86%D9%8A%D9%87_%25D9%2584%D9%84%D8%A7%D9%8A%D9%81%D9%88%D9%86.txt/file"
IPHONE_CODES_PDF_LINK = "https://www.mediafire.com/file/buaehs8iyroqqvt/LATEST_ICCID_CODE_-_Problem_Killer_%25282%2529.pdf/file"

# ================= 3. واجهة Web App (الثيم المعدني + التصفح الداخلي) =================
"""
HMAX UNLOCKER - نسخة نهائية تعمل 100% على Render
- بدون أخطاء استيراد
- الموقع مضيء متحرك
- /health يرجع JSON
"""
app = Flask(__name__)

# ===== HMAX LIGHTING SYSTEM - مدمج بدون ملف خارجي =====
NEON_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700&display=swap');
body{margin:0;background:radial-gradient(circle at 20% 30%,#0a1931 0%,#000 100%);font-family:'Cairo',sans-serif;color:#fff;min-height:100vh}
.neon-title{font-size:2.8em;text-align:center;margin-top:35px;text-shadow:0 0 10px #00f0ff,0 0 20px #00f0ff,0 0 40px #00f0ff;animation:glow 2s infinite alternate}
@keyframes glow{from{text-shadow:0 0 10px #00f0ff}to{text-shadow:0 0 20px #00f0ff,0 0 60px #00f0ff}}
.card{background:rgba(0,240,255,0.06);border:1px solid rgba(0,240,255,0.3);box-shadow:0 0 15px rgba(0,240,255,0.15);border-radius:16px;padding:20px;margin:12px;min-width:210px;display:inline-block;transition:.3s}
.card:hover{box-shadow:0 0 25px #00f0ff,0 0 50px rgba(0,240,255,.3);transform:translateY(-5px)}
.btn{background:linear-gradient(45deg,#00f0ff,#0080ff);box-shadow:0 0 12px #00f0ff;padding:11px 26px;border-radius:30px;color:#fff;text-decoration:none;display:inline-block;font-weight:bold;margin-top:8px}
.beam{position:fixed;top:0;width:2px;height:100vh;background:linear-gradient(to bottom,transparent,#00f0ff,transparent);animation:move 4s infinite linear;opacity:.5}
@keyframes move{0%{left:-5%}100%{left:105%}}
.dot{width:12px;height:12px;background:#00ff88;border-radius:50%;box-shadow:0 0 10px #00ff88,0 0 20px #00ff88;animation:pulse 1.5s infinite;display:inline-block}
@keyframes pulse{0%{transform:scale(1)}50%{transform:scale(1.3)}100%{transform:scale(1)}}
</style>
"""

def get_home_html():
    return f"""<!DOCTYPE html><html dir="rtl" lang="ar"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>HMAX LIGHTING</title>{NEON_CSS}</head>
<body><div class="beam"></div>
<div style="text-align:center;padding:25px">
<h1 class="neon-title">✨ HMAX UNLOCKER ✨</h1>
<p style="color:#00f0ff;letter-spacing:3px">LIGHTING SYSTEM ACTIVE • تم تفعيل الإضاءة بنجاح</p>
<div style="margin:20px"><span class="dot"></span> النظام مضيء <span class="dot"></span></div>
<div style="margin-top:30px">
<div class="card"><h3>🤖 بوت تيليجرام</h3><p>🟢 Online</p><a class="btn" href="https://t.me/haithamMax1">القناة</a></div>
<div class="card"><h3>💡 API</h3><p>/api • /health • /light</p><a class="btn" href="/api">API</a></div>
<div class="card"><h3>🌟 الإضاءة</h3><p>Neon Active</p><span class="btn">ON 💡</span></div>
</div>
<p style="margin-top:35px;color:#666;font-size:.85em">للـ JSON القديم استخدم <code>/?json=1</code> • للإضاءة <code>/?light=1</code></p>
</div></body></html>"""

@app.route('/')
def home():
    # إذا طلب json=1 ارجع JSON القديم عشان البوت والـ health check ما يخرب
    if request.args.get("json") == "1" or request.args.get("format") == "json":
        return jsonify({"status": "ok","service": "HMAX-UNLOCKER","mode": "telegram-bot-api"})
    # افتراضياً اعرض الإضاءة
    return render_template_string(get_home_html())

@app.route('/health')
def health():
    return jsonify({"status": "ok"})

@app.route('/light')
@app.route('/neon')
def light_page():
    return render_template_string(get_home_html())

@app.route('/json')
def json_home():
    return jsonify({"status": "ok","service": "HMAX-UNLOCKER","mode": "telegram-bot-api"})

# ================= 🆕 HMAX كأداة API - إضافة بدون حذف أي شيء قديم =================
@app.route('/api')
def api_home():
    try:
        total = sum(len(v) for v in DATA.values()) if 'DATA' in globals() else 0
    except:
        total = 0
    return jsonify({
        "status": "HMAX Tool API ✅",
        "bot": "HMAX-UNLOCKER",
        "mode": "bot+tool",
        "total_categories": len(DATA) if 'DATA' in globals() else 0,
        "total_tools": total,
        "owner": "Haitham Max @haithamMax1",
        "endpoints": ["/api/categories", "/api/tools", "/api/search?q=", "/api/tool/<id>", "/api/iphone/codes", "/api/openapi.json"]
    })

@app.route('/api/categories')
def api_categories():
    return jsonify({"categories": list(DATA.keys())})

@app.route('/api/tools')
def api_tools():
    def safe_unpack(v):
        if isinstance(v, (list, tuple)):
            name = v[0] if len(v) > 0 else "Unknown"
            url = v[1] if len(v) > 1 else ""
            return name, url
        return str(v), ""
    cat = request.args.get("category")
    if cat and cat in DATA:
        tools = {}
        for tid, val in DATA[cat].items():
            try:
                name, url = safe_unpack(val)
                tools[tid] = {"name": name, "url": url}
            except:
                continue
        return jsonify({"category": cat, "count": len(tools), "tools": tools})
    all_tools = {}
    for c, tools in DATA.items():
        for tid, val in tools.items():
            try:
                name, url = safe_unpack(val)
                all_tools[tid] = {"name": name, "url": url, "category": c}
            except:
                continue
    return jsonify({"count": len(all_tools), "tools": all_tools})

@app.route('/api/search')
def api_search():
    try:
        q = request.args.get("q", "").lower()
        if not q:
            return jsonify({"error": "أضف ?q=كلمة البحث مثل ?q=samfw | ?q=chimera | ?q=mtk"}), 400
        results = []
        for c, tools in DATA.items():
            for tid, val in tools.items():
                try:
                    if isinstance(val, (list, tuple)):
                        name = str(val[0]) if len(val) > 0 else ""
                        url = str(val[1]) if len(val) > 1 else ""
                    else:
                        name = str(val)
                        url = ""
                    if q in tid.lower() or q in name.lower():
                        results.append({"id": tid, "name": name, "url": url, "category": c})
                except Exception:
                    continue
        return jsonify({"query": q, "found": len(results), "results": results[:30]})
    except Exception as e:
        return jsonify({"error": f"Search error: {str(e)}", "query": request.args.get("q","")}), 500

@app.route('/api/tool/<tool_id>')
def api_tool(tool_id):
    def safe_unpack(v):
        if isinstance(v, (list, tuple)):
            name = v[0] if len(v) > 0 else "Unknown"
            url = v[1] if len(v) > 1 else ""
            extra = v[2] if len(v) > 2 else None
            return name, url, extra
        return str(v), "", None
    # بحث دقيق
    for c, tools in DATA.items():
        if tool_id in tools:
            try:
                name, url, extra = safe_unpack(tools[tool_id])
                resp = {"id": tool_id, "name": name, "url": url, "category": c}
                if extra:
                    resp["extra_url"] = extra
                return jsonify(resp)
            except:
                pass
    # بحث مقارب
    for c, tools in DATA.items():
        for tid, val in tools.items():
            try:
                name, url, extra = safe_unpack(val)
                if tool_id.lower() in tid.lower() or tool_id.lower() in name.lower():
                    resp = {"id": tid, "name": name, "url": url, "category": c, "matched": "partial"}
                    if extra:
                        resp["extra_url"] = extra
                    return jsonify(resp)
            except:
                continue
    return jsonify({"error": "الأداة غير موجودة", "tip": "جرب /api/search?q=اسم الأداة"}), 404

@app.route('/api/dump-tools')
def api_dump_tools():
    """فهرس أدوات سحب الدامب: روابط تحميل الأداة + بطاقاتها.

    /api/dump-tools                    كل الأدوات
    /api/dump-tools?category=jtag      أدوات JTAG فقط (أو normal)
    /api/dump-tools?tool=pandora       أداة واحدة مع بطاقاتها
    /api/dump-tools?q=realme           بحث في الأسماء والبطاقات
    ?lang=ar|en|fr لتحديد اللغة (الافتراضي ar)
    """
    try:
        import hmax_dump_tools as _hdt
    except Exception as exc:  # pragma: no cover - guards the old import crash
        return jsonify({"error": f"Dump tools module unavailable: {exc}"}), 503

    lang = request.args.get("lang", "ar")
    if lang not in ("ar", "en", "fr"):
        lang = "ar"
    category = request.args.get("category")
    if category and category not in ("jtag", "normal"):
        return jsonify({"error": "category must be 'jtag' or 'normal'"}), 400

    wanted_tool = request.args.get("tool")
    query = (request.args.get("q") or "").strip().lower()

    tools = []
    for key, tool in _hdt.DUMP_TOOLS.items():
        if category and tool.get("category") != category:
            continue
        if wanted_tool and key != wanted_tool:
            continue
        cards = [
            {"label": label.strip(), "callback": cb}
            for label, cb in _hdt.DUMP_CARDS.get(key, [])
        ]
        name = _hdt._loc(tool, "name", lang)
        if query:
            haystack = " ".join(
                [name, key, _hdt._loc(tool, "desc", lang)]
                + [c["label"] for c in cards]
            ).lower()
            if query not in haystack:
                continue
        tools.append({
            "id": key,
            "category": tool.get("category"),
            "icon": tool.get("icon"),
            "name": name,
            "description": _hdt._loc(tool, "desc", lang),
            "supported": _hdt._loc(tool, "supported", lang),
            "download_url": tool.get("url"),
            "download_label": _hdt._loc(tool, "btn", lang),
            "cards_count": len(cards),
            "cards": cards,
        })

    if wanted_tool and not tools:
        return jsonify({"error": "الأداة غير موجودة", "tip": "جرب /api/dump-tools"}), 404

    return jsonify({
        "lang": lang,
        "category": category,
        "count": len(tools),
        "total_cards": sum(t["cards_count"] for t in tools),
        "tools": tools,
    })

@app.route('/api/iphone/codes')
def api_iphone_codes():
    codes = {
        "AT&T": ["3104101", "3131300", "3104108"],
        "Verizon": ["2040400", "3114806"],
        "Sprint": ["3160101", "3101200"],
        "Cricket": ["3101508", "3101500"],
        "YemenMobile": ["42102", "42101"]
    }
    carrier = request.args.get("carrier", "").lower()
    if carrier:
        for k, v in codes.items():
            if carrier in k.lower():
                return jsonify({"carrier": k, "codes": v, "instruction": "استخدم الكود في SamFw Tool > تغيير CSC"})
        return jsonify({"available": list(codes.keys()), "message": "جرب ?carrier=att أو verizon أو yemen"})
    return jsonify(codes)

@app.route('/api/openapi.json')
def api_openapi():
    return jsonify({
        "openapi": "3.0.0",
        "info": {"title": "HMAX Tools API", "version": "2.0", "description": "أدوات هيثم ماكس كأداة للذكاء الاصطناعي"},
        "servers": [{"url": request.host_url.rstrip("/")}],
        "paths": {
            "/api/search": {"get": {"summary": "بحث عن أداة", "parameters": [{"name": "q", "in": "query", "required": True}]}},
            "/api/tool/{tool_id}": {"get": {"summary": "جلب أداة محددة"}},
            "/api/iphone/codes": {"get": {"summary": "أكواد الآيفون"}}
        }
    })

def run_flask():
    from waitress import serve
    serve(app, host='0.0.0.0', port=PORT, threads=8)

# سيتم تشغيل Flask بعد تحميل DATA بالكامل عند بدء الملف.


# ================= 5. بيانات الأدوات والروابط (نفسها) =================
DATA = {
    "tools": {
        "chimera":      ("🔧 Chimera Tool",       "https://chimeratool.com/ar/download"),
        "hydra":        ("🐉 Hydra Dongle",        "https://www.hydradongle.com/download/software"),
        "pandora":      ("📦 PANDORA Tool",        "https://downloads1.z3x.dev/getLatestVersion.php"),
        "qcdma":        ("📡 QCDMA TOOL",          "https://mega.nz/folder/fEQVBLab#1cPjBryW2_XPmqjxDoNZ0Q"),
        "cdma_yemen":   ("🇾🇪 CDMA YEMEN",         "https://www.mediafire.com/folder/kz5v059ycm44j/CDMA_YEMEN_TOOL"),
        "tsm_pro":      ("⭐ TSM Tool Pro",        "https://www.mediafire.com/file/vqh1h1uhwq9s2xo/TSM_SetupV2.4.1.7z/file"),
        "tsm_edition": ("✨ TSM PRO EDITION 2026.10.16 | Update", "https://www.mediafire.com/file/vqiuhtmypiv7gzs/TSM+Pro+Edition+Setup[2026.10.16].7z/file"),
        "dft_pro": ("🛠️ DFT Pro v8.0.0", "https://www.mediafire.com/file/m4ssk83p5wr5mxa/DFTPRO_v8.0.0.exe/file"),
        "sigma_main":   ("💎 Sigma Plus",          "https://sigmakey.com/nfs/content/5802/file/sigmaplus-software-setup-v1.01.13.exe"),
        "sigma_kirin":  ("📁 ات Kirin",         "https://mega.nz/file/HpgniKDT#OjCTB2_Ki_TxcKs7mCBNgd08eDVa1jPwOsU1aci0KXU"),
        "sigma_exynos": ("📁 ملفات Exynos",        "https://www.mediafire.com/file/fwqvfmq5om67t69/exynos.rar/file"),
        "unlock_tool":  ("🔓 UnlockTool", "https://file.unlocktool.net/"),
        "android_utility": ("🛠️ AndroidUtility v200", "https://www.mediafire.com/file/dp73po1rf9x4rgz/AndroidUtility.v200.7z/file"), # 🌟 السطر الجديد المضاف
    },
    "unlocking": {
        "global_unlocker": ("🌐 Global Unlocker",   "https://global-unlocker-pro.com/Download"),
        "tiraunlocker":    ("🔓 Tira Unlocker",     "http://www.tiraunlocker.com"),
        "fast_unlocker":   ("⚡ Fast Unlocker Pro", "https://fast-unlocker-pro.com/"),
        "q_unlocker":      ("🔑 Q-Unlocker",        "https://www.q-unlocker.com/"),
    },
    "ai_offers": {
        "gemini_12": ("💎 GEMINI PRO 12 شهر",  "تواصل للتفعيل"),
        "gemini_18": ("💎 GEMINI PRO 18 شهر",  "تواصل للتفعيل"),
        "gpt_plus":  ("🤖 GPT PLUS شهر واحد", "تواصل للتفعيل"),
        "gpt_go":    ("🤖 GPT GO سنة",         "تواصل للتفعيل"),
    },
    "drivers": {
        "adb":      ("🔌 Adb Driver",           "https://www.mediafire.com/file_premium/yx9pry29zxw0rsd/UniversalAdbDriverSetup.msi/file"),
        "mtk":      ("📲 MTK Driver",           "https://www.mediafire.com/file_premium/0psu8awm57or6jj/drivers_mtk_v2.0.1.1_2.7z/file"),
        "samsung":  ("📱 Samsung USB",          "https://www.mediafire.com/file_premium/92yzwgkkvkutye5/SAMSUNG_USB_Driver_for_Mobile_Phones_3.exe/file"),
        "fastboot": ("⚡ FASTBOOT DRIVER",      "https://mega.nz/file/w0plHSKZ#TjvkWuc9OmOpQiJq7Nr0U-ANlPVyf7RP1-2KvcgaSO4"),
        "exynos":   ("🔧 Exynos driver",        "https://mega.nz/file/ksYGmJ6T#_7DeakMDKI9lPkGIvUA0TIN9qHGCUtSrDfTDAump3WU"),
        "adb_fix":  ("🛠️ حل مشكلة ADB",        "https://mega.nz/file/UgZwSCRS#rgIJ8Wdli6yG_m6V7aWzJZmrVLIfHTrzQWZUhvU6Ums"),
        "qcom":     ("📡 تعاريف QCOM",          "https://www.mediafire.com/file_premium/huiyajts19ntc0y/drivers_qcom_v1.0.7z/file"),
        "com1":     ("🔌 تعاريف COM-1",         "https://mega.nz/file/M9IgjQxB#lPAouwiWNAwxPjfKuj0OQT1fqcplCKjyeCdIb7WFSqQ"),
        "spd":      ("📲 تعاريف SPD",           "https://www.mediafire.com/file_premium/faeoenrr0yjbj91/SPD_Driver_R4.20.0201_last_drivers.zip/file"),
        "mtk_fix":  ("🛠️ Driver-Mtk-Fix",       "https://www.mediafire.com/file_premium/cm92fbnnig76nn4/Driver-Mtk-Fix-ChuyenMobileGsm.zip/file"),
        "oneplus":  ("⚙️ OnePlus USB Drivers",  "https://www.mediafire.com/file/1l2vuh3c7pes193/OnePlus-USB-Drivers.zip/file"), # 🌟 مضاف جديد
        "mtp_fix":  ("🛠️ حل مشكلة عدم تعرف MTP", "https://www.mediafire.com/file/6ezxozqj73vnear/fix_mtp_by_halabtech.zip/file"), # 🌟 مضاف جديد
        "moto_fastboot": ("⚡ تعاريف FASTBOOT Motorola", "https://www.mediafire.com/file/5u9kpffk8r5tb7t/Motorola_Mobile_Drivers_64bit.msi/file"), # 🌟 
        "tsm_exynos_fix": ("🛠️ اصلاح تخطي للاكسنوس TSM", "https://www.mediafire.com/folder/9wcn6zcmqbkyk/MicrosoftMSVC"),
    },
    "halabtech_arabization": {
        # الترتيب: "المفتاح": ("الاسم المكتوب في الزر", "رابط الدعم الرسمي", "رابط التحميل المباشر")
        "t387v":  ("📱 SM-T387V U3 (Arabic)", "https://support.halabtech.com/index.php?a=downloads&b=file&id=104983", "https://www.mediafire.com/file/cfqitvgt28yi089/Setup_New_Translation_Language_HalabTech.rar/file"),
        "t377r4": ("📱 T377R4 7.0 Arabic Turkey 1 Min", "https://support.halabtech.com/index.php?a=downloads&b=file&id=104983", "https://drive.google.com/file/d/1Ws6OmwXHWFtwyE2r2iRYos2hLp2SqDjN/view"),
    },
       
    "iphone_tools": {
        "3utools_v3_28":  ("🛠️ 3utools V3.28",      "https://www.mediafire.com/file/peba8a9wshyi1bb/3utools-3-28-012.7z/file"),
        "3utools_latest": ("🚀 3utools آخر تحديث",  "https://www.mediafire.com/file/zruyfcl2aem7tjq/3utools-9-0-088.7z/file"),
        "itunes_paid":    ("🍎 itunes مدفوع",        "تواصل للتفعيل"),
    },
    "free_android": {
        "mobimover":       ("📲 برنامج نقل من هاتف لآخر",   "https://www.mediafire.com/file/ixrm0wgzm2zx64u/EaseUS.MobiMover.6.2.3.25122.rar/file"),
        "samfw_tool": ("🛠️ Samfw tool v6.0.1", "https://samfw.com/SamFwToolSetup_v6.0.1.zip"),
        "maxtech_vip":     ("✨ MaxTech VIP",               "https://mega.nz/file/XLRlVRDL#VwmnEJdpTDSB_TFEjA6YGdDJ8k6dgafs6ANgFTj3FW0"),
        "mysterious_dev":  ("🕵️ Mysterious-Dev Tool",       "https://mysterious-dev.com/download.html"),
        "honor_fastboot":  ("🔍 قراءة معلومات أجهزة الهونر بوضع الفاست بوت", "https://www.mediafire.com/file/8voavhswgbnz6dn/FastbootReader_2.zip/file"),
        "defender_control": ("🛡️ Defender_Control_v2.1", "https://www.mediafire.com/file_premium/r2jmxq0ps0ymq66/Defender_Control_v2.1.zip/file"),
        "activator_master": ("💻 0_Activator Master v8.0", "https://www.mediafire.com/file/7n00k39c4du7cvz/0_Activator_Master_v8.0_%2528Pass%253DMorocco%2529.zip/file"), # 🌟 السطر الجديد المضاف
    },
    "free_iphone": {
        "3utools_v3_28":  ("🛠️ 3utools V3.28",     "https://www.mediafire.com/file/peba8a9wshyi1bb/3utools-3-28-012.7z/file"),
        "3utools_latest": ("🚀 3utools آخر تحديث", "https://www.mediafire.com/file/zruyfcl2aem7tjq/3utools-9-0-088.7z/file"),
        "itunes_12_13_9": ("🍏 iTunes 12.13.9 (64-bit)", "https://www.mediafire.com/file/whfr41knzymf2n9/itunes-64-bit-12-13-9-1.exe/file"), # 🌟 السطر الجديد المضاف
    },
    "firmware_sites": {
        "samsung":  ("📱 أنظمة السامسونج", "https://samfw.com/"),
        "lg":       ("📱 أنظمة LG",        "https://lgrom.com/"),
        "xiaomi":   ("📱 أنظمة شاومي",    "https://mifirm.net/"),
        "realme":   ("📱 أنظمة Realme",   "https://romprovider.com/firmware/realme/"),
        "oneplus":  ("📱 OnePlus",         "https://androidmtk.com/download-oneplus-stock-rom-for-all-models"),
        "oppo":     ("📱 أنظمة Oppo",     "https://firmwarefile.com/category/oppo"),
        "trecfone": ("📱 أنظمة TRECFONE", "https://www.mediafire.com/folder/2z9cmetgup90m/TrecFone_Firmware"),
        "vivo":     ("📱 أنظمة Vivo",     "https://androidmtk.com/download-vivo-stock-rom"),
        "motorola": ("📱 أنظمة Motorola", "https://androidmtk.com/download-motorola-stock-rom-for-all-models"),
        "zte":      ("📱 أنظمة ZTE",      "https://androidmtk.com/download-zte-stock-rom-for-all-models"),
        "itel":     ("📱 أنظمة Itel",     "https://androidmtk.com/download-itel-stock-rom"),
        "honor":    ("📱 أنظمة Honor",    "https://firmwarefile.com/category/honor/page/2"),
    },
}

# ================= 🌟 قاعدة بيانات عروض هيثم ماكس الكاملة =================
all_hitham_products = {
    'capcut_1m': "📦 *العرض:* حساب Capcut Pro لمدة شهر (ضمان كامل) 🎬\n💵 *السعر:* حسب الطلب\n\n📝 • حساب رسمي مفعل عليه باقة Pro لمدة شهر كامل.\n• 🔓 فتح جميع الفلاتر والتأثيرات.\n• 🛡️ الضمان: شهر كامل.",
    'capcut_3m': "📦 *العرض:* حساب Capcut Pro لمدة 3 أشهر (ضمان كامل) 🎬\n💵 *السعر:* حسب الطلب\n\n📝 • حساب رسمي مفعل Pro لمدة 3 أشهر.\n• 🛡️ الضمان: 3 أشهر.",
    'capcut_6m': "📦 *العرض:* حساب Capcut Pro لمدة 6 أشهر (ضمان كامل) 🎬\n💵 *السعر:* حسب الطلب\n\n📝 • حساب رسمي مفعل Pro لمدة 6 أشهر.\n• 🛡️ الضمان: 6 أشهر.",
    'capcut_1y': "📦 *العرض:* حساب Capcut Pro لمدة سنة (ضمان كامل) 🎬\n💵 *السعر:* حسب الطلب\n\n📝 • حساب رسمي مفعل Pro لمدة 12 شهراً.\n• 🛡️ الضمان: سنة كاملة.",
    'canva_1y': "📦 *العرض:* مقعد كانفا برو (Canva Pro) لمدة سنة 🎨\n💵 *السعر:* $8\n\n📝 • مقعد رسمي يتم تفعيله على إيميلك الشخصي.\n• 🛡️ ضمان شامل لمدة سنة.",
    'yt_6m': "📦 *العرض:* مقعد يوتيوب بريميوم لمدة 6 أشهر ▶️\n💵 *السعر:* $11\n\n📝 • ترقية خلال 5 ثوانٍ.\n• 🛡️ دعم فني 12 شهراً.",
    'yt_12m': "📦 *العرض:* مقعد يوتيوب بريميوم مخصص - 12 شهراً ▶️\n💵 *السعر:* $25\n\n📝 • حساب مخصص ومستقر بالكامل عبر عدة أجهزة.\n• 🛡️ الضمان: سنة كاملة.",
    'cursor_200': "📦 *العرض:* API Cursor Pro 200 Credits/day 🖱️\n💵 *السعر:* $18\n\n📝 • 200 نقطة يومياً.\n• 🛡️ الضمان: 30 يوماً.",
    'cursor_2600': "📦 *العرض:* API Cursor Pro 2600 Credits 🖱️\n💵 *السعر:* $15\n\n📝 • 2600 نقطة إجمالية للشهر.\n• 🛡️ الضمان: 30 يوماً.",
    'cursor_6500': "📦 *العرض:* API Cursor Pro 6500 Credits 🖱️\n💵 *السعر:* $18\n\n📝 • 6500 نقطة إجمالية للشهر.\n• 🛡️ الضمان: 30 يوماً.",
    'lovable_1m': "📦 *العرض:* حساب Lovable AI PRO لمدة شهر ✨\n💵 *السعر:* $20\n\n📝 • اشتراك PRO الرسمي.\n• 🛡️ الضمان: 30 يوماً.",
    'lovable_lite': "📦 *العرض:* حساب Loveable Pro Lite لمدة سنة ✨\n💵 *السعر:* $10\n\n📝 • رصيد 300 نقطة.\n• 🛡️ الضمان: شهر واحد.",
    'figma_edu': "📦 *العرض:* حساب Figma Pro Education لمدة سنة 🎨\n💵 *السعر:* $11\n\n📝 • باقة تعليمية بصلاحيات Pro و 3000 نقطة شهرياً.\n• 🛡️ الضمان: سنة.",
    'leonardo_ai': "📦 *العرض:* حساب Leonardo AI برصيد 8,500 نقطة 🎨\n💵 *السعر:* $5\n\n📝 • رصيد 8500 نقطة.\n• 🛡️ الضمان: 24 ساعة.",
    'grok_1m': "📦 *العرض:* حساب Grok Super لمدة شهر ⚡\n💵 *السعر:* $18\n\n📝 • صيغة التسليم: إيميل وباسورد.\n• 🛡️ الضمان: شهر.",
    'grok_3m': "📦 *العرض:* حساب Grok Super لمدة 3 أشهر ⚡\n💵 *السعر:* $26\n\n📝 • 🛡️ الضمان: 3 أشهر.",
    'grok_6m': "📦 *العرض:* حساب Grok Super لمدة 6 أشهر ⚡\n💵 *السعر:* $40\n\n📝 • 🛡️ الضمان: 6 أشهر.",
    'grok_12m': "📦 *العرض:* حساب Grok Super لمدة 12 شهراً ⚡\n💵 *السعر:* $75\n\n📝 • 🛡️ الضمان: سنة كاملة.",
    'suno_pro': "📦 *العرض:* حساب SUNO PRO لمدة شهر 🎵\n💵 *السعر:* $12\n\n📝 • 2500 نقطة شهرياً مع حقوق تجارية.\n• 🛡️ الضمان: 7 أيام.",
    'elevenlabs': "📦 *العرض:* حساب Elevenlabs Creator برصيد 131K 🎙️\n💵 *السعر:* $12\n\n📝 • رصيد 131,000 حرف.\n• 🛡️ الضمان: 5 أيام.",
    'kling_ultra': "📦 *العرض:* حساب Kling Ultra 27.5K لمدة شهر 🎬\n💵 *السعر:* $85\n\n📝 • 27,500 نقطة. مع سياسة التعويض النسبي.\n• 🛡️ الضمان: 3 أيام.",
    
    # --- الإضافات الجديدة ---
    'netflix_1m': "📦 *العرض:* اشتراك Netflix Premium 4K لمدة شهر 🍿\n💵 *السعر:* $3.50\n\n📝 • أعلى باقة 4K، مع ملف شخصي (Profile) مستقل خاص بك للمشاهدة.\n• 📺 يدعم الهواتف، الكمبيوتر، الشاشات الذكية، والأجهزة الداعمة لنتفلكس.\n• 🔑 صيغة التسليم: (الحساب | الباسورد | اسم الملف الشخصي | باسورد الملف).\n\n🛡️ *الضمان:* ضمان كامل طوال فترة الاشتراك مع معالجة ودعم سريع لأي خلل.\n\n⚠️ *ملاحظات وشروط هامة:*\n- يرجى استخدام ملفك الشخصي (Profile) المخصص لك فقط.\n- يُمنع منعاً باتاً تغيير معلومات الحساب أو حذف/تعديل اسم الملف.\n- يُمنع تسجيل الدخول بأجهزة غريبة وكثيرة في نفس الوقت.\n- 🌐 للعملاء في الخارج: يلزم استخدام VPN/IP (فيتنامي) لضمان استقرار المشاهدة.",
    'gpt_plus_1m': "📦 *العرض:* حساب CHAT GPT PLUS لمدة شهر (ضمان كامل) 🤖\n💵 *السعر:* $9.91\n\n📝 • حسابات تجريبية مستقرة جداً تعتمد على امتدادات Gmail موثوقة.\n• يتم تحديث الحسابات المدفوعة يومياً لضمان استقرار فترة الصلاحية وتجنب تلاعب التواريخ.\n• 🔑 صيغة التسليم: (الإيميل | الباسورد | رمز المصادقة الثنائية 2FA).\n\n⚠️ *الضمان والشروط الهامة (يرجى القراءة بعناية):*\n- لك الصلاحية لتغيير كلمة المرور الخاصة بك.\n- **يُمنع منعاً باتاً** تغيير رمز المصادقة الثنائية (2FA)؛ تغييره يلغي الضمان فوراً.\n- بسبب حملات الحظر الحالية على حسابات GPT، يُرجى فور استلام الحساب: فحص الحساب، تغيير الباسورد، وتفعيل الـ 2FA الخاص بك مع حفظ الباسورد في مكان آمن.\n- 🔄 إذا نسيت الباسورد وكان إيميلك فعالاً، يمكنني مساعدتك في استرجاعه.\n- 🚫 إذا تم حظر الحساب كلياً (Account Dead) أو نسيت البيانات، لا يمكنني تقديم الدعم أو التعويض.",
    'gpt_plus_level_30d': "📦 *العرض:* حساب ChatGPT Plus مستوى 30 يوماً (ضمان كامل) 🤖\n💵 *السعر:* $9.91\n\n📝 • حسابات تجريبية مدفوعة عبر (Apple Pay فيتنام) مع امتداد Gmail باستقرار ممتاز.\n• يتم تحديث الحسابات المدفوعة يومياً لضمان استقرار تاريخ الصلاحية.\n• 🔑 صيغة التسليم: (الإيميل | الباسورد | 2FA).\n• 🔐 للحصول على كود تسجيل الدخول من الـ 2FA، استخدم الموقع: `2fa.live`\n• 📱 في حال واجهت مشكلة طلب رقم هاتف، يمكنك استئجار رقم عبر `viotp.com` (اختر خدمة Chatgpt + شبكة Vina).\n\n⚠️ *تنبيهات وضمانات هامة:*\n- نظراً لوجود حملات فحص لحسابات GPT، يُرجى فور استلام الحساب فحصه، ثم **تغيير الباسورد وتفعيل الـ 2FA الخاص بك فوراً** مع تدوين الباسورد الجديد.\n- 🔄 إذا نسيت الباسورد وكان الإيميل فعالاً (Live)، سأقوم بمساعدتك في استرجاعه.\n- 🚫 إذا تم حظر الحساب كلياً (Account Dead)، فلن أتمكن من تقديم الدعم.",
    'gpt_plus_apple_pay_30d': "📦 *العرض:* حساب ChatGPT Plus Apple Pay لمدة 30 يوماً (ضمان كامل) 🤖\n💵 *السعر:* $9.913\n\n📝 • حسابات مدفوعة عبر (Apple Pay فيتنام) بامتداد Gmail، وتتميز باستقرار ومتانة عالية جداً (Super Durable).\n• يتم تحديث الحسابات بمنتجات جديدة يومياً.\n• 🔑 صيغة التسليم: (الإيميل | الباسورد | رمز 2FA).\n• 🔐 للحصول على كود تسجيل الدخول من الـ 2FA، استخدم الموقع: `2fa.live`\n• 📱 في حال أردت استخدام Codex واحتجت لتفعيل رقم، يمكنك استئجاره عبر `viotp.com` (اختر خدمة Chatgpt + شبكة Vina).\n\n⚠️ *شروط الضمان:*\n- يرجى فحص الحساب (الباسورد والـ 2FA) فور الشراء للتأكد من عمله.\n- إذا قمت بتغيير الباسورد أو إعدادات الـ 2FA الخاصة بالحساب، يخرج الحساب من الضمان ولا يتم التعويض.",
    'gpt_plus_apple_pay_1m_1d': "📦 *العرض:* حساب ChatGPT Plus (ApplePay) لمدة شهر (ضمان 24 ساعة) 🤖\n💵 *السعر:* $8.77\n\n📝 • الحساب مفعّل باشتراك Apple Pay (بإيميل iCloud أو Gmail).\n• 🔑 صيغة التسليم: (الإيميل | الباسورد | رمز 2FA).\n\n⚙️ *تعليمات تسجيل الدخول:*\n1️⃣ اذهب إلى صفحة الدخول: `https://auth.openai.com/log-in` وأدخل الإيميل.\n2️⃣ أدخل الباسورد.\n3️⃣ للحصول على كود الـ 2FA: ادخل إلى الموقع `https://2fa.live`، الصق الكود المعطى لك واضغط Submit لنسخ الأرقام الستة الأخيرة.\n\n⚠️ *ملاحظات وشروط الضمان (ضمان يوم واحد فقط):*\n- يمكنك تغيير الباسورد وإعدادات الـ 2FA بحريّتك، ولكن **إذا نسيته لن نتمكن من مساعدتك في استرجاعه**.\n- الدعم والضمان يشمل تسجيل الدخول لـ ChatGPT فقط (لا يوجد ضمان لخدمات Codex أو 9Router).\n- إذا احتجت للتحقق برقم هاتف لـ (Codex)، يمكنك استئجار رقم عبر موقع `viotp.com`.",
}

# ================= نصوص الأقسام =================
LT_FREE_1_DESC = (
    "**📂 أنظمة LT مجانية رقم 1**\n\n"
    "**📱 الموديلات المدعومة:**\n"
    "▫️ LT 8103 - M205\n▫️ LT 9906\n▫️ LT C26 - M105\n"
    "▫️ It m15 (4+64)\n▫️ LT-E18 - M15 PLUS\n▫️ LT-E16 - M10 PLUS\n"
    "▫️ M20 PLUS - LT M8501\n▫️ M30 PLUS - E6707LT\n\n"
    "🔗 رابط التحميل المباشر أدناه:"
)
LT_FREE_2_DESC = (
    "**📂 أنظمة LT مجانية رقم 2**\n\n"
    "**📱 الموديلات المدعومة:**\n"
    "▫️ LT M20 Android 13\n▫️ LT M30 S22 Android 13\n▫️ LT M50S S33\n"
    "▫️ M25 - M30S - M40 - M50 - M60 - M70\n\n"
    "🔗 رابط التحميل المباشر أدناه:"
)
ICLOUD_PRICES = (
    "**💰 قائمة الأسعار المحدثة لفتح الآيكلود رسمي:**\n\n"
    "📱 iPhone 11 series: **(100$)**\n"
    "📱 iPhone 12 series: **(115$)**\n"
    "📱 iPhone 13 series: **(125$)**\n"
    "📱 iPhone 14 series: **(135$)**\n"
    "📱 iPhone 15 series: **(150$)**\n"
    "📱 iPhone 16 series: **(175$)**\n"
    "📱 iPhone 17 series: **(250$)**\n\n"
    "⏳ **وقت الخدمة:** 20-30 يوم\n"
    "━━━━━━━━━━━━━━━━━\n"
    "✅ للتفعيل تواصل مع الإدارة."
)
ITUNES_PAID_DESC = (
    "**🍎 itunes مدفوع**\n\n"
    "هذه الخدمة تتيح لك تنزيل التطبيقات والألعاب من iTunes إلى اللابتوب "
    "وتثبيتها على أي جهاز.\n\n"
    "✅ لطلب الخدمة تواصل معنا عبر الأزرار أدناه:"
)
MOBIMOVER_DESC = (
    "**📲 برنامج نقل من هاتف لآخر**\n\n"
    "يتيح نقل الرسائل والملفات والصور من iPhone إلى Android والعكس.\n\n"
    "🔗 رابط التحميل المباشر أدناه:"
)
MAXTECH_VIP_DESC = (
    "**✨ أداة تعريب ومميزات - MaxTech Server VIP**\n\n"
    "هدية من فريق ماكس تك وهيثم ماكس\n\n"
    "👤 **تطوير:** عاهد الحلياني و بشير ياسر\n"
    "🤝 **بمساعدة:** هيثم ماكس، وسيم ناصر، خالد مجدي، فراس الصراري\n\n"
    "**📱 مميزات الإصدار V2.0:**\n\n"
    "**1️⃣ تعريب سامسونج الشامل:**\n"
    "   ▫️ دعم أندرويد 15 و 16\n"
    "   ▫️ تعريب أندرويد 14، 13 (One UI 5.1)\n"
    "   ▫️ حلول من أندرويد 9 إلى 13\n\n"
    "**2️⃣ خدمات إضافية:**\n"
    "   ▫️ تفعيل VoLTE و IMS سامسونج\n"
    "   ▫️ إظهار أيقونة 4G/5G المفقودة\n"
    "   ▫️ حذف الإعلانات وإصلاح التعريب\n\n"
    "**3️⃣ دعم الأجهزة القديمة:**\n"
    "   ▫️ تعريب أندرويد 6، 7، 8\n\n"
    "💪 فريق MAX TECH SERVER يضع القوة بين يديك!"
)

SAMSUNG_EXYNOS_GIFT_DESC = (
    "**🎁 FRP SAMSUNG All Model EXYNOS - مجاني**\n\n"
    "✨ طريقة تخطي FRP وKG لجميع معالجات Exynos\n"
    "📱 يدعم أندرويد 14/15/16 وحماية 2025/2026\n\n"
    "**📍 الخطوات عبر برنامج MobilEdit:**\n\n"
    "1️⃣ افتح برنامج MobilEdit\n"
    "2️⃣ اضغط على (بدء)\n"
    "3️⃣ اختر (التجاوز الأمني)\n"
    "4️⃣ اختر (حسب الشريحة)\n"
    "5️⃣ اختر نوع المعالج حسب موديل الجهاز\n"
    "6️⃣ اضغط بدء وقم بتوصيل الجهاز في Download Mode\n"
    "7️⃣ انتظر حتى يُعيد التشغيل وتظهر رسالة الاسترداد\n"
    "8️⃣ أغلق MobilEdit واستخدم أي برنامج يدعم ADB FRP\n"
    "9️⃣ فعّل خيار المطور وانتظر عملية التخطي\n\n"
    "**🛠️ البرامج المجربة:**\n"
    "▫️ TSM TOOL\n▫️ CDMA Yemen Tool Pro\n▫️ Unlock Tool\n\n"
    "🔗 رابط التحميل أدناه:"
)

# 🔚 نهاية الجزء 1️⃣
# ================= 6. الدوال المساعدة =================

# ====================================================================================
# 🛡️ دالات الحماية، النقاط، ومستقبلات الطلبات المركزية (المدمجة والمطورة) 🚀
# ====================================================================================

def is_subscribed(user_id, force_refresh=False):
    """التحقق من الاشتراك الإجباري مع cache قصير وتحديث فوري عند طلب المستخدم."""
    uid = str(user_id)
    if int(uid) == MY_CHAT_ID:
        return True

    if not force_refresh:
        cached = _SUBSCRIPTION_CACHE.get(uid)
        if cached is not None:
            return cached

    try:
        member = bot.get_chat_member(CHANNEL_ID, int(uid))
        status = getattr(member, "status", "")

        if status in {"member", "administrator", "creator"}:
            is_member = True
        elif status == "restricted":
            is_member = bool(getattr(member, "is_member", False))
        else:
            is_member = False

        _SUBSCRIPTION_CACHE.set(uid, is_member)
        return is_member
    except Exception as e:
        print(f"⚠️ فشل التحقق من الاشتراك للمستخدم {uid}: {e}")
        return False


def is_user_banned(user_id):
    """التحقق من الحظر محلياً وبـFirebase مع cache قصير لنتائج Firebase."""
    uid = str(user_id)

    if uid in get_banned_users():
        BANNED_USERS.set_status(uid, True)
        return True

    cached = BANNED_USERS.get_status(uid)
    if cached is not None:
        return cached

    try:
        if db:
            user_ref = db.collection("users").document(uid).get()
            if user_ref.exists:
                banned = (user_ref.to_dict() or {}).get("is_banned", 0) == 1
                BANNED_USERS.set_status(uid, banned)
                return banned
            BANNED_USERS.set_status(uid, False)
    except Exception as e:
        print(f"خطأ في التحقق من الحظر: {e}")

    return False


def get_user_data(user_id):
    """🆕 جلب جميع بيانات المستخدم"""
    try:
        if db:
            doc = db.collection('users').document(str(user_id)).get()
            if doc.exists:
                return doc.to_dict()
    except Exception as e:
        print(f"خطأ في جلب بيانات المستخدم: {e}")
    return {}

def get_user_points(user_id):
    """جلب نقاط المستخدم"""
    data = get_user_data(user_id)
    return data.get('points', 0)

def add_points(user_id, points):
    """إضافة نقاط للمستخدم"""
    try:
        if db:
            db.collection('users').document(str(user_id)).set(
                {'points': firestore.Increment(points)}, merge=True
            )
    except Exception as e:
        print(f"خطأ في إضافة النقاط: {e}")

def increment_click():
    """زيادة عداد النقرات الكلي"""
    try:
        if db:
            db.collection('stats').document('clicks').set(
                {'value': firestore.Increment(1)}, merge=True
            )
    except:
        pass

def increment_daily_stat(stat_name):
    """🆕 زيادة إحصائية يومية"""
    try:
        if db:
            today = str(datetime.date.today())
            db.collection('daily_stats').document(today).set(
                {stat_name: firestore.Increment(1)}, merge=True
            )
    except Exception as e:
        print(f"خطأ في الإحصائيات اليومية: {e}")

def track_tool(tool_name, user_id=None):
    """🆕 تتبع استخدام الأداة + منح نقاط + تسجيل التفاعل"""
    try:
        if db:
            db.collection('tool_usage').document(tool_name).set(
                {'count': firestore.Increment(1)}, merge=True
            )
            increment_daily_stat('tool_clicks')
        if user_id:
            rewarded = hmaxx.award_tool_reward(user_id, tool_name, POINTS_PER_ACTION["tool_click"])
            log_interaction(user_id, f"فتح: {tool_name}" + ("" if rewarded else " (بدون نقاط: حد اليوم)"))
    except Exception as e:
        print(f"خطأ في تتبع الأداة: {e}")

def log_interaction(user_id, action_name):
    """🆕 تسجيل تفاعل المستخدم في Firebase"""
    try:
        if db:
            db.collection('user_interactions').add({
                "user_id": user_id,
                "action": action_name,
                "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "date_only": str(datetime.date.today())
            })
    except Exception as e:
        print(f"خطأ في تسجيل التفاعل: {e}")

def get_local_today():
    """تاريخ اليوم بحسب توقيت اليمن (UTC+3)."""
    yemen_tz = datetime.timezone(datetime.timedelta(hours=3))
    return datetime.datetime.now(datetime.timezone.utc).astimezone(yemen_tz).date()


def check_daily_bonus(user_id):
    """منح نقاط الزيارة اليومية مرة واحدة فقط بشكل ذري في Firebase."""
    if not db:
        return False

    try:
        today = str(get_local_today())
        user_ref = db.collection("users").document(str(user_id))
        transaction = db.transaction()

        @firestore.transactional
        def apply_daily_bonus(txn):
            snapshot = user_ref.get(transaction=txn)
            if not snapshot.exists:
                return False

            data = snapshot.to_dict() or {}
            if data.get("last_daily_visit", "") == today:
                return False

            txn.set(
                user_ref,
                {
                    "last_daily_visit": today,
                    "points": firestore.Increment(POINTS_PER_ACTION["daily_visit"]),
                },
                merge=True,
            )
            return True

        return bool(apply_daily_bonus(transaction))
    except Exception as e:
        print(f"خطأ في مكافأة الزيارة اليومية: {e}")
        return False

# 🆕 [إضافة حصرية]: الدالة المركزية لتوليد ملف بيانات المستخدم الكامل للأدمن لايف
def get_user_admin_profile_html(user_id):
    """توليد كتلة بيانات ملف المستخدم الكاملة والحقيقية للأدمن بنظام HTML 🚀"""
    data = get_user_data(user_id)
    if not data:
        return f"👤 <b>بيانات العضو:</b> آيدي <code>{user_id}</code> (لم تكتمل بياناته بداخل فايربيز بعد)"
    
    pts = data.get('points', 0)
    full_name = data.get('full_name', 'مهندس صيانة')
    username = data.get('username', '')
    joined = data.get('joined_date', 'غير معروف')
    rank_name, _ = get_rank(pts)
    
    username_text = f"@{username}" if username and username != "NoUsername" else "لا يوجد"
    
    interactions_count = 0
    try:
        if db:
            int_q = db.collection('user_interactions').where('user_id', '==', int(user_id)).count().get()
            interactions_count = int_q[0][0].value if int_q else 0
    except:
        pass

    profile_html = (
        f"<b>📊 ملف بيانات المستخدم الكاملة (HMAX Account):</b>\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"👤 <b>الاسم الحقيقي:</b> {full_name}\n"
        f"🔹 <b>اليوزر حَقه:</b> {username_text}\n"
        f"🆔 <b>الآيدي (ID):</b> <code>{user_id}</code>\n"
        f"🏆 <b>المرتبة الحالية:</b> <b>{rank_name}</b>\n"
        f"💎 <b>رصيد النقاط:</b> <code>{pts}</code> نقطة\n"
        f"📈 <b>عدد المشاركات والتفاعلات:</b> <code>{interactions_count}</code> مرة\n"
        f"📅 <b>تاريخ الانضمام للمنظومة:</b> <code>{joined}</code>\n"
        f"━━━━━━━━━━━━━━━━━━"
    )
    return profile_html

# 🆕 [تحديث ذكي]: إشعار الأدمن بدخول العضو مع سحب تفاصيل هويته الكاملة
def notify_admin_new_user(user_id, username, full_name, inviter_id=None):
    """إشعار الأدمن بدخول مستخدم جديد مع كامل تفاصيل هويته وبياناته السيرفرية"""
    try:
        inviter_text = f"\n🔗 <b>دخل عبر رابط دعوة الآيدي:</b> <code>{inviter_id}</code>" if inviter_id else ""
        user_profile_data = get_user_admin_profile_html(user_id)
        
        final_msg = (
            f"🔔 <b>انضمام عضو جديد كلياً للمنظومة!</b>\n\n"
            f"{user_profile_data}"
            f"{inviter_text}"
        )
        
        markup_reply = types.InlineKeyboardMarkup()
        markup_reply.add(types.InlineKeyboardButton("💬 مراسلة خاصة", callback_data=f"reply_req_{user_id}"))
        bot.send_message(MY_CHAT_ID, final_msg, reply_markup=markup_reply, parse_mode="HTML")
    except:
        pass

# 🆕 [إضافة حصرية]: دالة إطلاق الانتظار لطلب السيريال وصورة الأداة للآيفون
def request_s_unlocker(message, category):
    """فتح خطوة استقبال طلب الآيفون مع السيريال والصورة/التعليق."""
    user_id = message.chat.id
    if int(user_id) != MY_CHAT_ID and is_user_banned(user_id):
        bot.send_message(user_id, "🚫 تم حظرك من استخدام النظام.")
        return

    try:
        msg = bot.send_message(
            user_id,
            f"📝 <b>يرجى إرسال رقم السيريال (Serial) وصورة من الأداة معاً لخدمة {category}:</b>\n\n"
            "<i>يمكنك إرسال السيريال كنص، أو صورة مع السيريال في الوصف، أو اكتب \"إلغاء\".</i>",
            parse_mode="HTML"
        )
        bot.register_next_step_handler(msg, lambda m: process_iphone_request(m, category))
    except Exception as e:
        print(f"❌ خطأ في بدء طلب الآيفون: {e}")
        bot.send_message(user_id, "❌ تعذر بدء الطلب حالياً، حاول مرة أخرى.")

# 🆕 [إضافة حصرية]: دالة معالجة وحفظ طلب الآيفون وربطه بالتتبع الحي (Live Tracker) فورا
def process_iphone_request(message, category):
    """استقبال طلب الآيفون، حفظه، تحديث الإحصائيات، وإشعار الأدمن والعميل."""
    user_id = message.chat.id

    if int(user_id) != MY_CHAT_ID and is_user_banned(user_id):
        bot.send_message(user_id, "🚫 تم حظرك من استخدام النظام.")
        return

    text_source = message.text or message.caption
    if text_source and text_source.strip() == "إلغاء":
        show_main_menu(user_id)
        return

    serial_code = text_source.strip() if text_source else "مرفق بداخل الصورة 📸"
    req_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    request_description = f"فتح شفرة آيفون [{category}]"

    if db:
        try:
            db.collection("user_requests").add({
                "user_id": int(user_id),
                "request_text": f"{request_description} | السيريال: {serial_code}",
                "request_date": req_date,
                "status": "قيد المراجعة ⏳",
                "request_type": "iphone_unlock",
            })
            db.collection("stats").document("requests").set(
                {"value": firestore.Increment(1)}, merge=True
            )
            increment_daily_stat("requests")
        except Exception as db_err:
            print(f"❌ خطأ تدوين طلب الآيفون بفايربيز: {db_err}")

    add_points(user_id, POINTS_PER_ACTION["request"])
    log_interaction(user_id, request_description)

    user_profile_data = get_user_admin_profile_html(user_id)
    text_to_admin = (
        "🔥 <b>طلب رفع وفك شفرة آيفون جديد!</b>\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"📱 <b>الخدمة المطلوبة:</b> {category}\n"
        f"🔢 <b>رقم السيريال (Serial):</b> <code>{telebot.util.escape_html(serial_code)}</code>\n"
        f"📅 <b>التوقيت الحالي:</b> {req_date}\n\n"
        f"{user_profile_data}"
    )

    markup_reply = types.InlineKeyboardMarkup()
    markup_reply.add(
        types.InlineKeyboardButton("💬 رد وتسليم فوري", callback_data=f"reply_req_{user_id}")
    )

    try:
        if message.photo:
            bot.send_photo(
                MY_CHAT_ID,
                message.photo[-1].file_id,
                caption=text_to_admin,
                reply_markup=markup_reply,
                parse_mode="HTML"
            )
        else:
            bot.send_message(
                MY_CHAT_ID, text_to_admin,
                reply_markup=markup_reply, parse_mode="HTML"
            )
    except Exception as e:
        print(f"❌ خطأ إرسال طلب الآيفون للأدمن: {e}")

    success_text = (
        "✅ <b>تم إرسال طلبك بنجاح إلى المنظومة السيرفرية!</b>\n\n"
        f"📱 <b>الخدمة المحددة:</b> {category}\n"
        f"🔢 <b>كود السيريال:</b> <code>{telebot.util.escape_html(serial_code)}</code>\n"
        "📊 <b>الحالة الحالية:</b> قيد المراجعة ⏳\n\n"
        "━━━━━━━━━━━━━━━━━━\n"
        f"🎁 حصلت على <b>+{POINTS_PER_ACTION['request']} نقطة</b> لهذا الطلب.\n"
        "📈 يمكنك متابعة حالة الطلب من زر <b>سجل تفاعلاتي</b> في القائمة الرئيسية."
    )
    try:
        bot.send_message(user_id, success_text, parse_mode="HTML")
    except Exception as e:
        print(f"❌ خطأ إرسال تأكيد طلب الآيفون للعميل: {e}")
    show_main_menu(user_id)

# 🆕 [إضافة حصرية]: دالة استقبال تعليق ومقترح التقييم وإرساله للأدمن بكامل تفاصيل الهوية
def save_rating_comment_step(message, stars):
    """حفظ تعليق التقييم وإرساله للأدمن مع بيانات المستخدم."""
    user_id = message.chat.id

    if not message.text:
        show_main_menu(user_id)
        return

    comment_text = message.text.strip()
    if comment_text == "إلغاء":
        show_main_menu(user_id)
        return

    if db:
        try:
            db.collection("users").document(str(user_id)).set(
                {"rating_comment": comment_text}, merge=True
            )
        except Exception as e:
            print(f"❌ خطأ في حفظ تعليق التقييم: {e}")

    try:
        escaped_comment = telebot.util.escape_html(comment_text)
        user_profile_data = get_user_admin_profile_html(user_id)
        markup_reply = types.InlineKeyboardMarkup()
        markup_reply.add(
            types.InlineKeyboardButton("💬 رد مباشر", callback_data=f"reply_req_{user_id}")
        )

        admin_msg = (
            "📝 <b>مقترح وتعليق جديد من التقييمات!</b>\n"
            f"⭐ <b>التقييم الممنوح:</b> {stars} نجوم\n"
            f"💬 <b>نص الرسالة:</b>\n<code>{escaped_comment}</code>\n\n"
            f"{user_profile_data}"
        )
        bot.send_message(
            MY_CHAT_ID, admin_msg,
            reply_markup=markup_reply, parse_mode="HTML"
        )
    except Exception as e:
        print(f"❌ خطأ في توجيه تعليق التقييم للأدمن: {e}")

    try:
        bot.send_message(
            user_id,
            "✅ <b>شكراً جزيلاً لك!</b> تم إرسال تعليقك ومقترحك بنجاح إلى الإدارة.",
            parse_mode="HTML"
        )
    except Exception as e:
        print(f"❌ خطأ إرسال تأكيد تعليق التقييم: {e}")
    show_main_menu(user_id)

def show_my_interactions(user_id):
    """عرض سجل موحد لآخر الطلبات والتفاعلات للمستخدم."""
    lines = [
        "📝 <b>سجل طلباتك وتفاعلاتك الحية</b>\n"
        "━━━━━━━━━━━━━━━━━━\n"
    ]
    has_data = False

    if db:
        try:
            request_docs = list(
                db.collection("user_requests")
                  .where('user_id', '==', int(user_id))
                  .limit(15).stream()
            )
            request_docs.sort(
                key=lambda d: str((d.to_dict() or {}).get("request_date", "")),
                reverse=True
            )

            if request_docs:
                has_data = True
                lines.append("📱 <b>آخر طلبات السيرفر والآيفون:</b>\n")
                for doc in request_docs:
                    data = doc.to_dict() or {}
                    req_text = data.get("request_text", "طلب خدمة")
                    status = data.get("status", "قيد المراجعة ⏳")
                    req_date = data.get("request_date", "")
                    lines.append(
                        f"• {req_text}\n"
                        f"  📊 <b>الحالة:</b> {status}\n"
                        f"  🕐 {req_date}\n"
                    )
                lines.append("━━━━━━━━━━━━━━━━━━\n")
        except Exception as e:
            print(f"❌ خطأ في جلب طلبات المستخدم: {e}")

        try:
            interaction_docs = list(
                db.collection("user_interactions")
                  .where('user_id', '==', int(user_id))
                  .limit(15).stream()
            )
            interaction_docs.sort(
                key=lambda d: str((d.to_dict() or {}).get("date", "")),
                reverse=True
            )

            if interaction_docs:
                has_data = True
                lines.append("⚙️ <b>آخر الأدوات والتفاعلات:</b>\n")
                for doc in interaction_docs:
                    data = doc.to_dict() or {}
                    action = data.get("action", "تصفح قسم")
                    when = data.get("date", "")
                    lines.append(f"• {action}" + (f" (🕐 {when})" if when else ""))
                lines.append("━━━━━━━━━━━━━━━━━━\n")
        except Exception as e:
            print(f"❌ خطأ في جلب تفاعلات المستخدم: {e}")

    if not has_data:
        lines.append(
            "ℹ️ <b>لا يوجد سجل تفاعلات أو طلبات حتى الآن.</b>\n"
            "ابدأ بتصفح الأدوات أو إرسال طلب خدمة لتظهر بياناتك هنا. 🚀"
        )

    lines.append("💡 يتم تحديث السجل من السيرفر عند تسجيل الطلبات والتفاعلات.")
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton("👤 ملفي الشخصي", callback_data="my_profile"),
        types.InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_start")
    )
    try:
        bot.send_message(
            user_id, "\n".join(lines),
            reply_markup=markup, parse_mode="HTML"
        )
    except Exception as e:
        print(f"❌ فشل إرسال سجل المستخدم: {e}")

# ================= 🆕 نظام استقبال طلبات الآيفون المجانية =================
# ================= 🆕 لوحات المفاتيح الثابتة =================

def _localize_reply_keyboard(kb, lang):
    """Translate reply-keyboard labels for ``lang``.

    telebot 4.14 stores ReplyKeyboardMarkup buttons as plain dicts, which the
    inline-markup translator in hmax_i18n does not visit, so they are handled here.
    """
    for row in kb.keyboard:
        for button in row:
            if isinstance(button, dict):
                button["text"] = hmaxi18n.translate_button(button.get("text", ""), lang)
            else:
                button.text = hmaxi18n.translate_button(button.text, lang)
    return kb


def get_user_reply_keyboard(lang="ar"):
    """⌨️ لوحة المفاتيح الثابتة للمستخدم العادي"""
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add(
        types.KeyboardButton("🏠 القائمة الرئيسية"),
        types.KeyboardButton("👤 حسابي ونقاطي")
    )
    kb.add(
        types.KeyboardButton("📝 سجل تفاعلاتي"),
        types.KeyboardButton("🎁 هدية لكم")
    )
    kb.add(
        types.KeyboardButton("📢 قناة الأخبار"),
        types.KeyboardButton("💬 تواصل معنا")
    )
    return _localize_reply_keyboard(kb, lang)

def get_admin_reply_keyboard(lang="ar"):
    """⌨️ لوحة المفاتيح الثابتة للأدمن"""
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    kb.add(
        types.KeyboardButton("🏠 القائمة الرئيسية"),
        types.KeyboardButton("⚙️ لوحة الأدمن")
    )
    kb.add(
        types.KeyboardButton("📊 إحصائيات يومية"),
        types.KeyboardButton("📢 رسالة جماعية")
    )
    kb.add(
        types.KeyboardButton("👥 قائمة المستخدمين"),
        types.KeyboardButton("📩 طلبات المستخدمين")
    )
    kb.add(
        types.KeyboardButton("🆕 نشر التحديثات"),
        types.KeyboardButton("👤 ملفي الشخصي")
    )
    return _localize_reply_keyboard(kb, lang)

# ================= 7. عرض القوائم =================

def set_bot_commands():
    """تعيين أوامر البوت"""
    try:
        commands = [
            types.BotCommand("start",     "🚀 Start / Démarrer / ابدأ"),
            types.BotCommand("help",      "❓ Help / Aide / المساعدة"),
            types.BotCommand("myprofile", "👤 My profile / Mon profil / ملفي"),
            types.BotCommand("points",    "💎 Points and referrals / Points et parrainage / النقاط والإحالات"),
            types.BotCommand("dashboard", "⚙️ Admin dashboard / Administration / لوحة الإدارة"),
            types.BotCommand("telegram",  "👤 Telegram support / Assistance Telegram / تواصل تليجرام"),
            types.BotCommand("whatsapp",  "📱 WhatsApp support / Assistance WhatsApp / تواصل واتساب"),
            types.BotCommand("search",    "🔎 Search tools / Rechercher / البحث عن أداة"),
            types.BotCommand("favorites", "⭐ Favorites / Favoris / المفضلة"),
            types.BotCommand("notify",    "🔔 Notifications / Notifications / الإشعارات"),
            types.BotCommand("coupon",    "🎟️ Points coupon / Coupon de points / كوبون نقاط"),
            types.BotCommand("vip",       "👑 VIP status / Statut VIP / حالة VIP"),
            types.BotCommand("streak",    "🔥 Daily streak / Série quotidienne / سلسلة الزيارات"),
            types.BotCommand("profile",   "👤 Profile / Profil / الملف الشخصي"),
            types.BotCommand("achievements", "🏆 Achievements / Succès / الإنجازات"),
            types.BotCommand("store",      "🛒 Points store / Boutique de points / متجر النقاط"),
            types.BotCommand("language",   "🌐 Language / Langue / اللغة"),
        ]
        bot.set_my_commands(commands)
        print("✅ تم تعيين أوامر البوت بنجاح!")
    except Exception as e:
        print(f"خطأ في تعيين الأوامر: {e}")


def show_subscription_check(chat_id):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("📢 رابط قناتي للاشتراك", url=CHANNEL_URL),
        types.InlineKeyboardButton("✅ التحقق من الاشتراك",  callback_data="check_sub"),
    )
    bot.send_message(
        chat_id,
        "⚠️ لتشغيل البوت، اشترك في القناة أولاً ثم اضغط زر التحقق.",
        reply_markup=markup
    )

def show_language_selection(chat_id):
    """Offer Arabic, English, or French and persist the user's choice."""
    markup = types.InlineKeyboardMarkup(row_width=1)
    for code, label in hmaxi18n.LANGUAGE_LABELS.items():
        markup.add(types.InlineKeyboardButton(label, callback_data=f"set_lang_{code}"))
    bot.send_message(
        chat_id,
        "🌐 اختر لغتك / Choose your language / Choisissez votre langue",
        reply_markup=markup,
    )

def show_main_menu(user_id):
    """Display the main menu using the user's selected language."""
    try:
        lang = hmaxi18n.get_language(user_id)
        translations = {
            "en": {
                "advertise": "📢 Advertise With Us",
                "drivers": "🔧 Drivers Section",
                "tools": "🧰 Tools Section",
                "unlocking": "🔓 Unlocking",
                "gift": "🎁 Gift for you",
                "iphone": "🍎 IPHONE",
                "solutions": "📦 Verified Phone Solutions",
                "halabtech": "🗂️ HalabTech Files",
                "firmware": "💾 Firmware Section",
                "paid_offers": "💰 Paid Offers",
                "haitham_offers": "🔥 Haitham Max Offers",
                "community": "🎯 Services & Community Center",
                "profile": "👤 My Profile",
                "notifications": "🔕 Disable Notifications",
                "language": "🌐 تغيير اللغة / Language / Langue",
                "admin": "⚙️ Admin Panel (Secret)",
                "welcome": "👑 **Welcome to HMAX UNLOCKER Advanced Center**\n\nChoose the section you need from the menu below:",
            },
            "fr": {
                "advertise": "📢 Annoncez avec nous",
                "drivers": "🔧 Section Pilotes",
                "tools": "🧰 Section Outils",
                "unlocking": "🔓 Déverrouillage",
                "gift": "🎁 Cadeau pour vous",
                "iphone": "🍎 IPHONE",
                "solutions": "📦 Solutions téléphoniques vérifiées",
                "halabtech": "🗂️ Fichiers HalabTech",
                "firmware": "💾 Section Systèmes",
                "paid_offers": "💰 Offres payantes",
                "haitham_offers": "🔥 Offres Haitham Max",
                "community": "🎯 Centre des services et des interactions",
                "profile": "👤 Mon profil",
                "notifications": "🔕 Désactiver les notifications",
                "language": "🌐 تغيير اللغة / Language / Langue",
                "admin": "⚙️ Panneau d'administration (secret)",
                "welcome": "👑 **Bienvenue au centre avancé HMAX UNLOCKER**\n\nChoisissez la section souhaitée dans le menu ci-dessous :",
            },
            "ar": {
                "advertise": "📢 أعلن معنا (سوق المبرمجين)",
                "drivers": "🔧 قسم التعاريف",
                "tools": "🧰 قسم الأدوات",
                "unlocking": "🔓 فك الشفرات",
                "gift": "🎁 هدية لكم",
                "iphone": "🍎 IPHONE",
                "solutions": "📦 حلول منقولة مضمونة",
                "halabtech": "🗂️ ملفات حلب تك",
                "firmware": "💾 قسم الأنظمة",
                "paid_offers": "💰 عروض مدفوعة",
                "haitham_offers": "🔥 عروض هيثم ماكس",
                "community": "🎯 مركز الخدمات والتفاعل",
                "profile": "👤 ملفي الشخصي",
                "notifications": "🔕 إيقاف الإشعارات",
                "language": "🌐 تغيير اللغة / Language / Langue",
                "admin": "⚙️ لوحة الإدارة (سرية)",
                "welcome": "👑 **أهلاً بك في مركز خدمات HMAX UNLOCKER المتطور**\n\nاختر القسم الذي تريده من القائمة أدناه:",
            },
        }
        labels = translations.get(lang, translations["ar"])
        markup = types.InlineKeyboardMarkup()

        markup.row(types.InlineKeyboardButton(labels["advertise"], callback_data="paid_ads_menu"))
        markup.row(
            types.InlineKeyboardButton(labels["drivers"], callback_data="main_drivers"),
            types.InlineKeyboardButton(labels["tools"], callback_data="menu_tools_section"),
        )
        markup.row(
            types.InlineKeyboardButton(labels["unlocking"], callback_data="main_unlocking"),
            types.InlineKeyboardButton(labels["gift"], callback_data="gift_section"),
        )
        markup.row(types.InlineKeyboardButton(labels["iphone"], callback_data="main_iphone"))
        markup.row(types.InlineKeyboardButton(labels["solutions"], callback_data="phone_solutions_main"))
        markup.row(
            types.InlineKeyboardButton(labels["halabtech"], callback_data="halabtech_req"),
            types.InlineKeyboardButton(labels["firmware"], callback_data="menu_systems_section"),
        )
        markup.row(
            types.InlineKeyboardButton(labels["paid_offers"], callback_data="main_paid_offers"),
            types.InlineKeyboardButton(labels["haitham_offers"], callback_data="haitham_offers"),
        )
        markup.row(types.InlineKeyboardButton(labels["community"], callback_data="community_services_menu"))
        markup.row(
            types.InlineKeyboardButton(labels["profile"], callback_data="my_profile"),
            types.InlineKeyboardButton(labels["notifications"], callback_data="unsubscribe_me"),
        )
        markup.row(types.InlineKeyboardButton(labels["language"], callback_data="change_lang"))

        admin_id = MY_CHAT_ID if "MY_CHAT_ID" in globals() else 0
        if int(user_id) == admin_id:
            markup.row(types.InlineKeyboardButton(labels["admin"], callback_data="admin_panel"))

        bot.send_message(
            user_id,
            labels["welcome"],
            reply_markup=markup,
            parse_mode="Markdown",
        )
    except Exception as e:
        print(f"❌ خطأ في القائمة الرئيسية: {e}")


def finish_start(user_id, full_name="", subscription_verified=False):
    """Continue the normal start flow after a language has been selected."""
    if not full_name:
        full_name = (get_user_data(user_id) or {}).get("full_name", "")
    got_bonus = False
    if subscription_verified or is_subscribed(user_id):
        got_bonus = check_daily_bonus(user_id)
        streak_info = hmaxx.sync_daily_streak(user_id) if got_bonus else {"streak": 0, "bonus": 0}
        welcome_text = f"👋 **أهلاً بك {full_name} في HMAX UNLOCKER**"
        if got_bonus:
            welcome_text += (
                f"\n\n🎁 **حصلت على +{POINTS_PER_ACTION['daily_visit']} نقطة** "
                f"كمكافأة الزيارة اليومية!"
            )
            if streak_info.get("streak", 0):
                welcome_text += f"\n🔥 سلسلة الزيارات: **{streak_info['streak']} يوم**"
            if streak_info.get("bonus", 0):
                welcome_text += f"\n🏆 مكافأة السلسلة: **+{streak_info['bonus']} نقطة**"
        is_admin = int(user_id) == MY_CHAT_ID
        kb_lang = hmaxi18n.get_language(user_id)
        reply_kb = get_admin_reply_keyboard(kb_lang) if is_admin else get_user_reply_keyboard(kb_lang)
        bot.send_message(user_id, welcome_text, reply_markup=reply_kb, parse_mode="Markdown")
        show_main_menu(user_id)
    else:
        show_subscription_check(user_id)


# ================= 🆕 عرض الملف الشخصي =================

def show_my_profile(chat_id):
    """عرض الملف الشخصي للمستخدم مع التصنيف والنقاط"""
    data = get_user_data(chat_id)
    pts = data.get('points', 0)
    full_name = data.get('full_name', 'مستخدم')
    username = data.get('username', '')
    joined = data.get('joined_date', 'غير معروف')

    rank_name, rank_key = get_rank(pts)
    next_threshold, next_rank = get_next_rank_info(pts)

    if next_threshold:
        needed = next_threshold - pts
        progress = f"📈 للوصول لـ **{next_rank}** تحتاج: `{needed}` نقطة"
    else:
        progress = "🏆 **تهانينا! وصلت لأعلى مستوى ممكن!**"

    try:
        ref_link = f"https://t.me/{bot.get_me().username}?start={chat_id}"
    except:
        ref_link = "غير متاح"

    username_text = f"@{username}" if username and username != "NoUsername" else "لا يوجد"

    text = (
        f"👤 **ملفك الشخصي - HMAX**\n"
        f"━━━━━━━━━━━━━━━━━━\n\n"
        f"🏆 **الرتبة:** {rank_name}\n"
        f"📛 **الاسم:** {full_name}\n"
        f"🔹 **اليوزر:** {username_text}\n"
        f"🆔 **الآيدي:** `{chat_id}`\n"
        f"💎 **النقاط:** `{pts}` نقطة\n"
        f"📅 **تاريخ الانضمام:** {joined}\n\n"
        f"{progress}\n\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"🔗 **رابط دعوتك الخاص:**\n`{ref_link}`\n\n"
        f"💡 احصل على **{INVITE_POINTS} نقاط** عن كل دعوة ناجحة!"
    )

    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🚀 مشاركة رابط الدعوة",
                                   url=f"https://t.me/share/url?url={ref_link}"),
        types.InlineKeyboardButton("📝 سجل تفاعلاتي", callback_data="my_interactions"),
    )
    markup.add(types.InlineKeyboardButton("🏠 رجوع للقائمة", callback_data="back_start"))
    bot.send_message(chat_id, text, reply_markup=markup, parse_mode="Markdown")




# ================= 🆕 سجل التفاعلات =================

# ================= 🆕 الإحصائيات اليومية =================

def show_daily_stats(chat_id):
    """عرض الإحصائيات اليومية للأدمن"""
    if int(chat_id) != MY_CHAT_ID:
        return

    today = str(datetime.date.today())
    yesterday = str(datetime.date.today() - datetime.timedelta(days=1))

    today_users = 0
    today_clicks = 0
    today_requests = 0
    today_interactions = 0
    yesterday_users = 0

    try:
        if db:
            # مستخدمو اليوم
            today_users_q = db.collection('users').where('joined_date', '==', today).count().get()
            today_users = today_users_q[0][0].value if today_users_q else 0

            # مستخدمو الأمس
            yest_users_q = db.collection('users').where('joined_date', '==', yesterday).count().get()
            yesterday_users = yest_users_q[0][0].value if yest_users_q else 0

            # إحصائيات اليوم
            daily_doc = db.collection('daily_stats').document(today).get()
            if daily_doc.exists:
                dd = daily_doc.to_dict()
                today_clicks = dd.get('tool_clicks', 0)

            # طلبات اليوم
            req_q = db.collection('user_requests').where(
                'request_date', '>=', today
            ).count().get()
            today_requests = req_q[0][0].value if req_q else 0

            # تفاعلات اليوم
            int_q = db.collection('user_interactions').where(
                'date_only', '==', today
            ).count().get()
            today_interactions = int_q[0][0].value if int_q else 0
    except Exception as e:
        print(f"خطأ في الإحصائيات اليومية: {e}")

    # حساب التغيّر
    if yesterday_users > 0:
        diff = today_users - yesterday_users
        diff_emoji = "📈" if diff >= 0 else "📉"
        diff_text = f"{diff_emoji} ({'+' if diff >= 0 else ''}{diff} عن الأمس)"
    else:
        diff_text = ""

    text = (
        f"📊 **الإحصائيات اليومية**\n"
        f"📅 التاريخ: `{today}`\n"
        f"━━━━━━━━━━━━━━━━━━\n\n"
        f"🆕 **مستخدمون جدد اليوم:** `{today_users}`\n"
        f"   {diff_text}\n\n"
        f"👆 **نقرات الأدوات:** `{today_clicks}`\n"
        f"📝 **طلبات جديدة:** `{today_requests}`\n"
        f"💬 **إجمالي التفاعلات:** `{today_interactions}`\n\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"⏰ آخر تحديث: {datetime.datetime.now().strftime('%H:%M:%S')}"
    )

    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🔄 تحديث", callback_data="refresh_daily_stats"),
        types.InlineKeyboardButton("📊 إحصائيات متقدمة", callback_data="admin_stats")
    )
    markup.add(types.InlineKeyboardButton("🏠 رجوع", callback_data="admin_panel"))
    bot.send_message(chat_id, text, reply_markup=markup, parse_mode="Markdown")

# ================= 8. معالجة الأوامر =================

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    if not hmaxx.allow_user(user_id, "start"):
        return
    username = message.from_user.username or "NoUsername"
    full_name = message.from_user.first_name or ""
    if message.from_user.last_name:
        full_name += f" {message.from_user.last_name}"

    args = message.text.split()
    inviter_id = int(args[1]) if len(args) > 1 and args[1].isdigit() else None
    created_new_user = False
    valid_inviter_id = None

    # --- إنشاء المستخدم بشكل ذري لمنع تكرار مكافأة الإحالة ---
    if db:
        try:
            user_ref = db.collection("users").document(str(user_id))
            transaction = db.transaction()

            @firestore.transactional
            def ensure_user_once(txn):
                snapshot = user_ref.get(transaction=txn)
                if snapshot.exists:
                    return False, snapshot.to_dict() or {}

                candidate_inviter = None
                if inviter_id and inviter_id != user_id:
                    inviter_ref = db.collection("users").document(str(inviter_id))
                    inviter_snapshot = inviter_ref.get(transaction=txn)
                    inviter_data = inviter_snapshot.to_dict() if inviter_snapshot.exists else {}
                    if inviter_snapshot.exists and inviter_data.get("is_banned", 0) != 1:
                        candidate_inviter = inviter_id

                user_data = {
                    "id": user_id,
                    "full_name": full_name,
                    "username": username,
                    "is_banned": 0,
                    "points": 0,
                    "joined_date": str(get_local_today()),
                    "inviter": candidate_inviter,
                    "last_daily_visit": "",
                    "is_subscribed": True,
                }
                txn.set(user_ref, user_data)
                return True, user_data

            created_new_user, created_data = ensure_user_once(transaction)
            valid_inviter_id = created_data.get("inviter") if created_new_user else None

            if created_new_user:
                notify_admin_new_user(user_id, username, full_name, valid_inviter_id)

                # مكافأة إحالة ذرية: نفس الدعوة لا يمكن مكافأتها مرتين.
                if valid_inviter_id:
                    reward_id = f"{valid_inviter_id}_{user_id}"
                    reward_ref = db.collection("referral_rewards").document(reward_id)
                    reward_transaction = db.transaction()

                    @firestore.transactional
                    def apply_referral_reward(txn):
                        reward_snapshot = reward_ref.get(transaction=txn)
                        if reward_snapshot.exists:
                            return False

                        inviter_ref = db.collection("users").document(str(valid_inviter_id))
                        inviter_snapshot = inviter_ref.get(transaction=txn)
                        inviter_data = inviter_snapshot.to_dict() if inviter_snapshot.exists else {}

                        if not inviter_snapshot.exists or inviter_data.get("is_banned", 0) == 1:
                            return False

                        txn.set(
                            reward_ref,
                            {
                                "inviter_id": valid_inviter_id,
                                "invited_user_id": user_id,
                                "points": POINTS_PER_ACTION["invite"],
                                "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                            },
                        )
                        txn.set(
                            inviter_ref,
                            {"points": firestore.Increment(POINTS_PER_ACTION["invite"])},
                            merge=True,
                        )
                        return True

                    rewarded = bool(apply_referral_reward(reward_transaction))

                    if rewarded:
                        log_interaction(valid_inviter_id, f"دعوة عضو جديد: {full_name}")
                        try:
                            escaped_name = telebot.util.escape_html(full_name)
                            bot.send_message(
                                valid_inviter_id,
                                f"🔔 <b>دخل مستخدم جديد عبر رابط الدعوة حَقك!</b>\n\n"
                                f"👤 <b>العضو:</b> {escaped_name}\n"
                                f"🎁 تم منحك <b>+{POINTS_PER_ACTION['invite']} نقطة</b> مرة واحدة فقط. 🚀",
                                parse_mode="HTML"
                            )
                        except Exception:
                            pass
            else:
                user_ref.update({
                    "full_name": full_name,
                    "username": username
                })
        except Exception as e:
            print(f"خطأ في حفظ/إحالة المستخدم: {e}")

    # --- التحقق من الحظر ---
    if is_user_banned(user_id):
        bot.send_message(user_id, "🚫 تم حظرك من استخدام البوت.")
        return

    log_interaction(user_id, "تشغيل البوت /start")
    if not hmaxi18n.has_language(user_id):
        show_language_selection(user_id)
        return
    finish_start(user_id, full_name)


@bot.message_handler(commands=["language"])
def language_command(message):
    show_language_selection(message.chat.id)


@bot.message_handler(commands=['help'])
def help_command(message):
    text = (
        "📚 **مساعدة - HMAX System**\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        "**📋 الأوامر المتاحة:**\n\n"
        "🚀 /start - تشغيل البوت\n"
        "🌐 /language - تغيير لغة البوت\n"
        "👤 /myprofile - ملفي الشخصي\n"
        "💎 /points - نقاطي ورابط الدعوة\n"
        "📱 /telegram - تواصل تليجرام\n"
        "📞 /whatsapp - تواصل واتساب\n"
        "⚙️ /dashboard - لوحة التحكم (للإدارة)\n\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "**💎 كيف تكسب النقاط؟**\n\n"
        f"🎁 +{POINTS_PER_ACTION['invite']} نقاط لكل دعوة ناجحة\n"
        f"📅 +{POINTS_PER_ACTION['daily_visit']} نقاط للزيارة اليومية\n"
        f"📝 +{POINTS_PER_ACTION['request']} نقاط لكل طلب\n"
        f"👆 +{POINTS_PER_ACTION['tool_click']} نقاط لكل أداة تستخدمها\n\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "**🏆 نظام الرتب:**\n\n"
        "⚪ عضو جديد (0+)\n"
        "🟢 عضو نشط (50+)\n"
        "🔵 عضو متميز (150+)\n"
        "🟡 عضو ذهبي (300+)\n"
        "🟣 عضو بلاتيني (600+)\n"
        "👑 VIP ملكي (1200+)"
    )
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="back_start"))
    bot.reply_to(message, text, parse_mode="Markdown", reply_markup=markup)


@bot.message_handler(commands=['myprofile'])
def myprofile_command(message):
    show_my_profile(message.chat.id)


@bot.message_handler(commands=['points'])
def points_command(message):
    show_my_profile(message.chat.id)


@bot.message_handler(commands=['telegram'])
def send_telegram_contact(message):
    bot.reply_to(message, f"👤 يمكنك التواصل معي عبر تليجرام:\n{TELEGRAM_ADMIN}")


@bot.message_handler(commands=['whatsapp'])
def send_whatsapp_contact(message):
    bot.reply_to(message, f"📱 يمكنك التواصل معي عبر واتساب:\n{WHATSAPP_URL}")


@bot.message_handler(commands=['dashboard'])
def admin_dashboard(message):
    if int(message.chat.id) == MY_CHAT_ID:
        show_admin_panel(message.chat.id)
    else:
        bot.reply_to(message, "❌ عذراً، هذا الأمر مخصص للإدارة فقط.")


# ================= 🆕 معالج الرسائل النصية (الكيبورد السفلي) =================

@bot.message_handler(
    func=lambda m: (
        m.text
        and not m.text.startswith('/')
        and not (m.chat.id == MY_CHAT_ID and m.reply_to_message)
    ),
    content_types=['text']
)
def handle_text_messages(message):
    """معالج أزرار الكيبورد السفلي الثابت المطور والمحمي"""
    user_id = message.chat.id
    if not hmaxx.allow_user(user_id, "message"):
        return
    text = hmaxi18n.normalize_reply_button(user_id, message.text.strip())
    is_admin = (int(user_id) == MY_CHAT_ID)

    # 🛡️ 1. حارس البوابة: فحص لو كان المستخدم محظوراً يتم طرده فوراً وتجميده
    if is_user_banned(user_id):
        bot.send_message(user_id, "🚫 **عذراً، لقد تم حظرك من استخدام هذا البوت بواسطة الإدارة.**")
        return

    # ===== ⚙️ 2. أوامر الإدارة الخاصة بالتحكم بالحظر (متوافقة مع فلتر البوت) =====
    if is_admin:
        # أمر عرض قائمة المحظورين الحالية
        if text == "📋 المحظورين":
            banned_list = get_all_banned_users()
            if not banned_list:
                bot.send_message(user_id, "✅ **قائمة المحظورين فارغة حالياً، لا يوجد أحد محظور.**")
            else:
                formatted_list = "\n".join([f"• `{uid}`" for uid in banned_list])
                bot.send_message(user_id, f"📋 **قائمة المستخدمين المحظورين حالياً:**\n\n{formatted_list}\n\n💡 *لفك الحظر أرسل كرسالة:* `فك حظر آيدي_المستخدم`", parse_mode="Markdown")
            return

        # أمر حظر مستخدم جديد عبر الكلمات المباشرة
        elif text.startswith("حظر "):
            target_id = text.replace("حظر ", "").strip()
            if target_id.isdigit():
                if ban_user_id(target_id):
                    bot.send_message(user_id, f"🚫 **تم حظر المستخدم صاحب الآيدي:** `{target_id}` **بنجاح.**", parse_mode="Markdown")
                else:
                    bot.send_message(user_id, "⚠️ تم تطبيق الحظر محلياً، لكن تعذر حفظه في Firebase.")
            else:
                bot.send_message(user_id, "❌ يرجى إدخال آيدي صحيح (أرقام فقط). مثال: `حظر 1234567`")
            return

        # أمر فك الحظر (الفتح) عن مستخدم
        elif text.startswith("فك حظر "):
            target_id = text.replace("فك حظر ", "").strip()
            if target_id.isdigit():
                if unban_user_id(target_id):
                    bot.send_message(user_id, f"🟢 **تم فك الحظر والفتح عن المستخدم صاحب الآيدي:** `{target_id}` **بنجاح!**", parse_mode="Markdown")
                else:
                    bot.send_message(user_id, "❌ تعذر فك الحظر في Firebase، لذلك بقي المستخدم محظوراً.")
            else:
                bot.send_message(user_id, "❌ يرجى إدخال آيدي صحيح. مثال: `فك حظر 1234567`")
            return

   # ===== 👥 3. أزرار المستخدم العادي الأساسية =====
    if text == "🏠 القائمة الرئيسية":
        show_main_menu(user_id)

    elif text == "👤 حسابي ونقاطي" or text == "👤 ملفي الشخصي":
        show_my_profile(user_id)

    elif text == "📝 سجل تفاعلاتي":
        show_my_interactions(user_id)

    # ===== 🎁 قسم هدية لكم (من الكيبورد السفلي) =====
    elif text == "🎁 هدية لكم":
        try: log_interaction(user_id, "دخول قسم الهدايا")
        except: pass
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("📱 عرض شاشة الآيفون على الكمبيوتر مجاناً + تفعيل", callback_data="gift_iphone_screen_mirror"),
            types.InlineKeyboardButton("🎬 أفضل برنامج لتصوير شاشة اللابتوب", callback_data="gift_screen_recorder"),
            types.InlineKeyboardButton("💢 أداة تخطي الآيكلاود مجاناً لمعالجات A5 (تجريبي)", callback_data="gift_icloud_a5"),
            types.InlineKeyboardButton("📺 برنامج للايفون لمشاهدة قنوات كاس العالم مجانا", callback_data="iphone_worldcup_app"),
            types.InlineKeyboardButton("🎁 Adobe Creative Cloud", callback_data="adobe_cloud_gift"),
            types.InlineKeyboardButton("🎁 FRP SAMSUNG All Model EXYNOS", callback_data="page_gift_samsung_exynos"),
            types.InlineKeyboardButton("🔍 بوت كاشف الأرقام", callback_data="number_detector"),
            types.InlineKeyboardButton("🎁 FMI OFF - Open Menu", callback_data="gift_fmi_off"),
            types.InlineKeyboardButton("📱 تخطي الايفون 1/9/2026 iOS 9.0x الى iOS 27.x", callback_data="gift_iphone_bypass"),
            types.InlineKeyboardButton("🔙 رجوع", callback_data="back_start")
        )
        bot.send_message(user_id, "🎁 **قسم هدية لكم:**\nأفضل الحلول الحصرية والمجانية بين يديك:", reply_markup=markup, parse_mode="Markdown")
        return
    
    elif text == "📢 قناة الأخبار":
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("🟢 واتساب 1", url=WHATSAPP_CHANNEL_1),
            types.InlineKeyboardButton("🟢 واتساب 2", url=WHATSAPP_CHANNEL_2)
        )
        markup.add(types.InlineKeyboardButton("🔵 قناة التيلجرام", url=CHANNEL_URL))
        bot.send_message(user_id, "📢 **قنوات الأخبار والتوثيقات:**", reply_markup=markup, parse_mode="Markdown")

    elif text == "💬 تواصل معنا":
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("📱 واتساب",  url=WHATSAPP_URL),
            types.InlineKeyboardButton("👤 تيلجرام", url=TELEGRAM_ADMIN)
        )
        bot.send_message(user_id, "💬 **اختر وسيلة التواصل:**", reply_markup=markup, parse_mode="Markdown")

    # ===== أزرار الأدمن =====
    elif text == "⚙️ لوحة الأدمن" and is_admin:
        show_admin_panel(user_id)

    elif text == "📊 إحصائيات يومية" and is_admin:
        show_daily_stats(user_id)

    elif text == "📢 رسالة جماعية" and is_admin:
        msg = bot.send_message(user_id, "📢 أرسل الرسالة للتعميم (أو اكتب 'إلغاء'):")
        bot.register_next_step_handler(msg, perform_broadcast)

    elif text == "👥 قائمة المستخدمين" and is_admin:
        show_admin_users_list(user_id)

    elif text == "📩 طلبات المستخدمين" and is_admin:
        show_all_user_requests_simple(user_id)

    elif text == "🆕 نشر التحديثات" and is_admin:
        status_msg = bot.send_message(user_id, "⏳ جاري الاتصال بالفايربيز وسحب النص ونشره...")
        threading.Thread(
            target=_broadcast_update_with_status,
            args=(user_id, status_msg.message_id),
            daemon=True,
        ).start()



def show_advanced_stats(chat_id, message_id):
    """عرض الإحصائيات المتقدمة مع التقييمات والإحالات والاستخدام."""
    if int(chat_id) != MY_CHAT_ID:
        return

    total_users = 0
    today_users = 0
    top_inviter = "لا يوجد"
    top_tool = "لا يوجد"
    requests_count = 0
    banned_count = 0
    clicks_count = 0
    interactions_count = 0
    total_stars = 0
    rating_count = 0
    avg_rating_text = "لا يوجد تقييمات بعد"

    try:
        if db:
            total_users = db.collection("users").count().get()[0][0].value
            today = str(datetime.date.today())
            today_users = db.collection("users").where(
                'joined_date', '==', today
            ).count().get()[0][0].value
            banned_count = db.collection("users").where(
                'is_banned', '==', 1
            ).count().get()[0][0].value

            try:
                for u_doc in db.collection("users").where(
                    'user_rating', '>', 0
                ).stream():
                    value = (u_doc.to_dict() or {}).get("user_rating", 0)
                    try:
                        total_stars += float(value)
                        rating_count += 1
                    except (TypeError, ValueError):
                        pass
                if rating_count:
                    avg_rating_text = f"{total_stars / rating_count:.2f} / 5 ⭐"
            except Exception as e:
                print(f"خطأ في حساب التقييمات: {e}")

            try:
                inviter_counts = {}
                for doc in db.collection("users").where(
                    'inviter', '>', 0
                ).stream():
                    inv = (doc.to_dict() or {}).get("inviter")
                    if inv:
                        inviter_counts[inv] = inviter_counts.get(inv, 0) + 1
                if inviter_counts:
                    best_id = max(inviter_counts, key=inviter_counts.get)
                    best_doc = db.collection("users").document(str(best_id)).get()
                    best_data = best_doc.to_dict() or {}
                    best_name = best_data.get("full_name", "غير معروف")
                    top_inviter = f"{best_name} ({inviter_counts[best_id]} عضو)"
            except Exception as e:
                print(f"خطأ في حساب الإحالات: {e}")

            try:
                tool_docs = db.collection("tool_usage").order_by(
                    "count", direction=firestore.Query.DESCENDING
                ).limit(1).get()
                if tool_docs:
                    t = tool_docs[0]
                    top_tool = f"{t.id} ({(t.to_dict() or {}).get('count', 0)} مرة)"
            except Exception as e:
                print(f"خطأ في حساب أكثر أداة استخداماً: {e}")

            try:
                req_doc = db.collection("stats").document("requests").get()
                if req_doc.exists:
                    requests_count = (req_doc.to_dict() or {}).get("value", 0)
            except Exception as e:
                print(f"خطأ في عداد الطلبات: {e}")

            try:
                click_doc = db.collection("stats").document("clicks").get()
                if click_doc.exists:
                    clicks_count = (click_doc.to_dict() or {}).get("value", 0)
            except Exception as e:
                print(f"خطأ في عداد النقرات: {e}")

            try:
                int_q = db.collection("user_interactions").count().get()
                interactions_count = int_q[0][0].value if int_q else 0
            except Exception as e:
                print(f"خطأ في عداد التفاعلات: {e}")
    except Exception as e:
        print(f"خطأ في الإحصائيات المتقدمة: {e}")

    text = (
        "📈 **لوحة الإحصائيات المتقدمة والتحليلات**\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        f"👥 إجمالي المستخدمين: `{total_users}`\n"
        f"🆕 مشتركو اليوم: `{today_users}`\n"
        f"🏆 أفضل داعي: {top_inviter}\n"
        f"⭐ أكثر أداة استخداماً: {top_tool}\n"
        f"📩 عدد الطلبات: `{requests_count}`\n"
        f"🚫 عدد المحظورين: `{banned_count}`\n"
        f"👆 عداد النقرات الكلي: `{clicks_count}`\n\n"
        "📊 **تحليلات التقييم العام للبوت:**\n"
        f"⭐ متوسط التقييم الحالي: `{avg_rating_text}`\n"
        f"👥 عدد المشاركين في التقييم: `{rating_count}` مستخدم\n"
        f"💬 إجمالي التفاعلات السيرفرية: `{interactions_count}`"
    )
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔙 رجوع لوحة الإدارة", callback_data="admin_panel"))
    try:
        bot.edit_message_text(
            text, chat_id, message_id,
            reply_markup=markup, parse_mode="Markdown"
        )
    except Exception:
        bot.send_message(
            chat_id, text,
            reply_markup=markup, parse_mode="Markdown"
        )

# ================= 9. معالج الأزرار Inline =================#


def _hmax_show_menu(call, text, markup, parse_mode=None):
    """Render a DUMP menu on the message that triggered the callback.

    The menu is edited in place when possible. When the message cannot be
    edited — most importantly when the user presses a back button while a
    *photo* dump card is on screen (Telegram cannot turn a photo into a
    text message) — the stale message is deleted and a fresh menu is sent,
    so the back button always lands on a working menu instead of failing
    silently or piling up duplicate messages.
    """
    chat_id = call.message.chat.id
    try:
        bot.edit_message_text(
            text,
            chat_id,
            call.message.message_id,
            reply_markup=markup,
            parse_mode=parse_mode,
        )
    except Exception as error:
        print(f"Edit DUMP menu failed ({error}); falling back to delete + send")
        try:
            bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
        except Exception:
            pass
        bot.send_message(chat_id, text, reply_markup=markup, parse_mode=parse_mode)


DUMP_SMART_SECTIONS = {
    "xiaomi_group": [],
    "jtag": [],
    "oppo": [],
    "vivo": [],
    "m_horse": [],
    "infinix": [],
}


def detect_brands(model):
    """Return every DUMP_SMART_SECTIONS bucket a model name belongs to.

    A single device can legitimately live in more than one section (for example
    "INFINIX HOT 40 Pro ... [M-HORSE]" is both an INFINIX and an M-HORSE card),
    so callers that only need the primary bucket use :func:`detect_brand`.
    """
    model_upper = model.upper()
    brands = []
    if any(brand in model_upper for brand in ("XIAOMI", "REDMI", "POCO")):
        brands.append("xiaomi_group")
    if "OPPO" in model_upper:
        brands.append("oppo")
    if "VIVO" in model_upper:
        brands.append("vivo")
    if "M-HORSE" in model_upper or "M_HORSE" in model_upper:
        brands.append("m_horse")
    if "INFINIX" in model_upper:
        brands.append("infinix")
    return tuple(brands)


def detect_brand(model):
    """Return the primary bucket for ``model`` (or ``None`` when unmatched)."""
    brands = detect_brands(model)
    return brands[0] if brands else None


def add_dump_smart(model, dumped_with, callback):
    dump_entry = (model, callback)
    for brand_section in detect_brands(model):
        DUMP_SMART_SECTIONS[brand_section].append(dump_entry)
    if "F64 ULTRA" in dumped_with.upper():
        DUMP_SMART_SECTIONS["jtag"].append(dump_entry)


# VIVO full-dump + NV catalogue supplied for the UnlockTool collection.
# Every item is shown only in the VIVO DUMP brand section, while the existing
# VIVO Y15s PD2140F 6.37.2 card keeps the same Drive file without duplication.
VIVO_UNLOCKTOOL_DUMPS = {
    "dump_model_vivo_y20s_g_y12s_fake_8_256": {
        "model": "Y20s [G] / Y12s",
        "menu": {
            "ar": "🔥 VIVO Y20s [G] / Y12s — 8+256GB [نسخة مقلدة]",
            "en": "🔥 VIVO Y20s [G] / Y12s — 8+256GB [FAKE]",
            "fr": "🔥 VIVO Y20s [G] / Y12s — 8+256GB [COPIE]",
        },
        "details": {
            "ar": "نسخة مقلدة (FAKE) • 8GB RAM + 256GB",
            "en": "FAKE / copy device • 8GB RAM + 256GB",
            "fr": "Appareil COPIE • 8GB RAM + 256GB",
        },
        "url": "https://drive.google.com/file/d/1-Umiavto0B6I3f2sRai9Qaci2k7PfRWj/view",
        "poster": "vivo_y20s_g_y12s_fake_8_256_unlocktool_nv.jpg",
    },
    "dump_model_vivo_y12s_v2026_pd2036f": {
        "model": "Y12s — V2026 — PD2036F",
        "menu": {
            "ar": "🔥 VIVO Y12s V2026 PD2036F — Full Dump + NV",
            "en": "🔥 VIVO Y12s V2026 PD2036F — Full Dump + NV",
            "fr": "🔥 VIVO Y12s V2026 PD2036F — Dump complet + NV",
        },
        "url": "https://drive.google.com/file/d/1Bbk56EkNG0Mxt5v6_h0jmNmWQbg-6uw-/view",
        "poster": "vivo_y12s_v2026_pd2036f_unlocktool_nv.jpg",
    },
    "dump_model_vivo_y100_v2239_pd2257f": {
        "model": "Y100 — V2239",
        "firmware": "PD2257F_EX_A_13.0.5.3.W30",
        "menu": {
            "ar": "🔥 VIVO Y100 V2239 — Full Dump + NV",
            "en": "🔥 VIVO Y100 V2239 — Full Dump + NV",
            "fr": "🔥 VIVO Y100 V2239 — Dump complet + NV",
        },
        "url": "https://drive.google.com/file/d/1euPnx7zmh9Q9p_aZpualyyw7ciF5AeFw/view",
        "poster": "vivo_y100_v2239_pd2257f_unlocktool_nv.jpg",
    },
    "dump_model_vivo_y53s_v2058_pd2103f": {
        "model": "Y53s — V2058 — PD2103F",
        "firmware": "PD2103F_EX_A_1.8.1",
        "menu": {
            "ar": "🔥 VIVO Y53s V2058 PD2103F — Full Dump + NV",
            "en": "🔥 VIVO Y53s V2058 PD2103F — Full Dump + NV",
            "fr": "🔥 VIVO Y53s V2058 PD2103F — Dump complet + NV",
        },
        "url": "https://drive.google.com/file/d/12j9rGKlKl3a9L-LCbJmBB0AWALy_t0da/view",
        "poster": "vivo_y53s_v2058_pd2103f_unlocktool_nv.jpg",
    },
    "dump_model_vivo_y75a": {
        "model": "Y75A",
        "menu": {
            "ar": "🔥 VIVO Y75A — Full Dump + NV",
            "en": "🔥 VIVO Y75A — Full Dump + NV",
            "fr": "🔥 VIVO Y75A — Dump complet + NV",
        },
        "url": "https://drive.google.com/file/d/1-XxEgR5FRyYhNYjQAT2of0ZGewvlNf2e/view",
        "poster": "vivo_y75a_unlocktool_nv.jpg",
    },
    "dump_model_vivo_y21_pd2139f": {
        "model": "Y21 — PD2139F",
        "firmware": "PD2139F_EX_A_6.25.6",
        "menu": {
            "ar": "🔥 VIVO Y21 PD2139F — Full Dump + NV",
            "en": "🔥 VIVO Y21 PD2139F — Full Dump + NV",
            "fr": "🔥 VIVO Y21 PD2139F — Dump complet + NV",
        },
        "url": "https://drive.google.com/file/d/1qpax6D1yamapS6ZlA7i52MXMm6pWENZU/view",
        "poster": "vivo_y21_pd2139f_unlocktool_nv.jpg",
    },
    "dump_model_vivo_v27e_v2237": {
        "model": "V27e — V2237",
        "menu": {
            "ar": "🔥 VIVO V27e V2237 — Full Dump + NV",
            "en": "🔥 VIVO V27e V2237 — Full Dump + NV",
            "fr": "🔥 VIVO V27e V2237 — Dump complet + NV",
        },
        "url": "https://drive.google.com/file/d/1sJdYeZPWctAnfDScxbiDBuKzv4RPGLGO/view",
        "poster": "vivo_v27e_v2237_unlocktool_nv.jpg",
    },
    "dump_model_vivo_y02s_v2203_pd2216f": {
        "model": "Y02s — V2203",
        "firmware": "PD2216F_EX_A_12.0.32.0.W20",
        "menu": {
            "ar": "🔥 VIVO Y02s V2203 — Full Dump + NV",
            "en": "🔥 VIVO Y02s V2203 — Full Dump + NV",
            "fr": "🔥 VIVO Y02s V2203 — Dump complet + NV",
        },
        "url": "https://drive.google.com/file/d/1Vv3DXV2CS0XtBpYtSCUt-iA8ZlO6YcHh/view",
        "poster": "vivo_y02s_v2203_pd2216f_unlocktool_nv.jpg",
    },
    "dump_model_vivo_y1s_pd2014f": {
        "model": "Y1s — PD2014F",
        "firmware": "PD2014F_EX_A_1.13.50",
        "menu": {
            "ar": "🔥 VIVO Y1s PD2014F — Full Dump + NV",
            "en": "🔥 VIVO Y1s PD2014F — Full Dump + NV",
            "fr": "🔥 VIVO Y1s PD2014F — Dump complet + NV",
        },
        "url": "https://drive.google.com/file/d/1p5SiaGVwU0LFGmYZ6dgyfJyV8aZwkA88/view",
        "poster": "vivo_y1s_pd2014f_unlocktool_nv.jpg",
    },
    "dump_model_vivo_y83_pd1803bf": {
        "model": "Y83 — PD1803BF",
        "firmware": "PD1803BF_EX_A_9.9.9",
        "menu": {
            "ar": "🔥 VIVO Y83 PD1803BF — Full Dump + NV",
            "en": "🔥 VIVO Y83 PD1803BF — Full Dump + NV",
            "fr": "🔥 VIVO Y83 PD1803BF — Dump complet + NV",
        },
        "url": "https://drive.google.com/file/d/1kzAc42uBYlwxW2F308aGFU4NJtoDc1c_/view",
        "poster": "vivo_y83_pd1803bf_unlocktool_nv.jpg",
    },
}

VIVO_UNLOCKTOOL_DUMP_CALLBACKS = (
    "dump_model_vivo_y20s_g_y12s_fake_8_256",
    "dump_model_vivo_y12s_v2026_pd2036f",
    "dump_model_vivo_y100_v2239_pd2257f",
    "dump_model_vivo_y53s_v2058_pd2103f",
    "dump_model_vivo_y75a",
    "dump_model_vivo_y21_pd2139f",
    "dump_model_vivo_v27e_v2237",
    "dump_model_vivo_y02s_v2203_pd2216f",
    "dump_model_vivo_y1s_pd2014f",
    "dump_model_vivo_y83_pd1803bf",
)


def vivo_unlocktool_dump_caption(dump, lang):
    """Build a compact, localized card caption for the VIVO UnlockTool set."""
    labels = {
        "ar": {
            "title": "دامب كامل + NV",
            "device": "الجهاز",
            "firmware": "الإصدار",
            "details": "التفاصيل",
            "file": "نوع الملف",
            "file_value": "ملف Full Dump + ملف NV",
            "tool": "الأداة",
            "hosting": "الاستضافة",
            "password": "كلمة المرور",
            "warning": "تأكد من تطابق الموديل والذاكرة والإصدار، وخذ نسخة احتياطية لبيانات الشبكة الخاصة بالجهاز قبل الكتابة.",
        },
        "en": {
            "title": "FULL DUMP + NV",
            "device": "Device",
            "firmware": "Firmware",
            "details": "Details",
            "file": "File type",
            "file_value": "Full Dump file + NV file",
            "tool": "Tool",
            "hosting": "Hosting",
            "password": "Password",
            "warning": "Confirm the exact model, storage and firmware, and back up the device’s own network data before writing.",
        },
        "fr": {
            "title": "DUMP COMPLET + NV",
            "device": "Appareil",
            "firmware": "Firmware",
            "details": "Détails",
            "file": "Type de fichier",
            "file_value": "Fichier dump complet + fichier NV",
            "tool": "Outil",
            "hosting": "Hébergement",
            "password": "Mot de passe",
            "warning": "Vérifiez le modèle, la mémoire et le firmware exacts, puis sauvegardez les données réseau de l’appareil avant l’écriture.",
        },
    }.get(lang, {})
    if not labels:
        return vivo_unlocktool_dump_caption(dump, "ar")

    lines = [
        f"🔥 VIVO {dump['model']} — {labels['title']} 🔥",
        "━━━━━━━━━━━━━━━━━━━━",
        f"📱 {labels['device']}: VIVO {dump['model']}",
    ]
    if dump.get("firmware"):
        lines.append(f"📌 {labels['firmware']}: {dump['firmware']}")
    if dump.get("details"):
        lines.append(f"🧩 {labels['details']}: {dump['details'].get(lang, dump['details']['ar'])}")
    lines.extend((
        f"📦 {labels['file']}: {labels['file_value']}",
        f"🛠️ {labels['tool']}: UnlockTool",
        f"☁️ {labels['hosting']}: Google Drive",
        f"🔐 {labels['password']}: MobiFirmware.VIP",
        "━━━━━━━━━━━━━━━━━━━━",
        f"⚠️ {labels['warning']}",
        "HMAX-UNLOCKER • HithamMax",
    ))
    return "\n".join(lines)


# ⚠️ TODO: replace with the real Google Drive link before this card ships.
INFINIX_HOT40_PRO_DRIVE_URL = (
    "https://drive.google.com/file/d/REPLACE_ME_INFINIX_HOT40_PRO_M_HORSE/view"
)

# ⚠️ TODO: replace with the real Google Drive link before this card ships.
REALME_C15_DRIVE_URL = (
    "https://drive.google.com/file/d/REPLACE_ME_REALME_C15_RMX2180/view"
)


add_dump_smart(
    "🔥 REDMI 9C M2006C3MG - 3GB [EASY JTAG]",
    "EASY JTAG PLUS",
    "dump_model_redmi_9c_m2006c3mg",
)
add_dump_smart(
    "🔥 Redmi A3x missi Android 16 - 4.5GB [AMT]",
    "AMT Tool",
    "dump_model_redmi_a3x_missi_android16",
)
add_dump_smart(
    "🔥 REDMI A3 C61 - 64GB - 3.6GB [F64 ULTRA]",
    "F64 ULTRA",
    "dump_model_redmi_a3_c61",
)
add_dump_smart(
    "🔥 REDMI 10A 220233L2G - 64GB [F64 ULTRA]",
    "F64 ULTRA",
    "dump_model_redmi_10a_220233l2g",
)
add_dump_smart(
    "🔥 REDMI 15C / POCO C85 - 256GB - 7.4GB [F64 ULTRA]",
    "F64 ULTRA",
    "dump_model_redmi_15c_poco_c85",
)
add_dump_smart(
    "🔥 REDMI Note 14 5G Beryl XML 6.5GB [EASY JTAG]",
    "EASY JTAG PLUS",
    "dump_model_redmi_note14_5g_beryl_xml",
)
add_dump_smart(
    "🔥 XIAOMI Redmi 13C (Gale) OS2.0.6.0.VGPMIXM [PANDORA]",
    "Pandora Tool",
    "dump_model_redmi_13c_gale",
)
add_dump_smart(
    "🔥 POCO C65 - 256GB [F64 ULTRA]",
    "F64 ULTRA",
    "dump_model_poco_c65_256gb",
)
add_dump_smart(
    "🔥 OPPO A57 CPH2387 [EASY JTAG PLUS]",
    "EASY JTAG PLUS",
    "dump_model_oppo_a57_cph2387",
)
add_dump_smart(
    "🔥 OPPO A54 CPH2239 C.33 Dead Boot [UnlockTool+NV]",
    "UnlockTool",
    "dump_model_oppo_a54_cph2239_dead_boot",
)

add_dump_smart(
    "🔥 OPPO A31 CPH2015 - 128GB eMMC DUMP | 2.4GB [EASY JTAG PLUS]",
    "EASY JTAG PLUS",
    "dump_model_oppo_a31_cph2015_128gb",
)

add_dump_smart(
    "🔥 OPPO RENO 12F 4G CPH2687 - 256GB [F64 BOX]",
    "F64 BOX",
    "dump_model_oppo_reno_12f_4g_cph2687",
)
add_dump_smart(
    "🔥 OPPO A6 PRO 5G CPH2781 11.A.31 - 128GB UFS [F64 BOX]",
    "F64 BOX",
    "dump_model_oppo_a6_pro_5g_cph2781",
)


add_dump_smart(
    "🔥 INFINIX NOTE 30 5G X6711 V600 - FULL DUMP [PANDORA]",
    "Pandora Tool",
    "dump_model_infinix_note_30_5g_x6711_v600",
)
add_dump_smart(
    "🔥 Infinix Smart 20 X6840B - FULL DUMP [UnlockTool]",
    "UnlockTool",
    "dump_model_x6840b_full_dump",
)
add_dump_smart(
    "🔥 Infinix Smart 6 X6511B - Factory Signed",
    "Factory Signed",
    "dump_model_x6511b_factory_signed",
)

add_dump_smart(
    "🔥 Infinix Smart 5 X657C Full + NV - 1.6GB [UnlockTool]",
    "Unlock Tool",
    "dump_model_infinix_x657c_smart5",
)

add_dump_smart(
    "🔥 VIVO Y03 - 4GB [EASY JTAG PLUS]",
    "EASY JTAG PLUS",
    "dump_model_vivo_y03_dump_4gb",
)
add_dump_smart(
    "🔥 VIVO Y04 V2430 - 10GB [EASY JTAG PLUS]",
    "EASY JTAG PLUS",
    "dump_model_vivo_y04_v2430_latest",
)
add_dump_smart(
    "🔥 VIVO Y04 V2430 (2) - OSv15 5GB [EASY JTAG PLUS]",
    "EASY JTAG PLUS",
    "dump_model_vivo_y04_v2430_2_osv15_easyjtag",
)
add_dump_smart(
    "🔥 VIVO Y21D PD2510F - 256GB UFS | 8.2GB [F64 ULTRA]",
    "F64 ULTRA",
    "dump_model_vivo_y21d_pd2510f",
)
add_dump_smart(
    "🔥 VIVO Y03T PD2360F - 64GB eMMC | 4.9GB [F64 ULTRA]",
    "F64 ULTRA",
    "dump_model_vivo_y03t_pd2360f",
)
add_dump_smart(
    "🔥 VIVO Y18 PD2327F - 128GB eMMC | 4.4GB [F64 ULTRA]",
    "F64 ULTRA",
    "dump_model_vivo_y18_pd2327f",
)
add_dump_smart(
    "📱 VIVO Y22S PD2228F - 128GB UFS [F64 BOX]",
    "F64 BOX",
    "dump_model_vivo_y22s_pd2228f",
)
add_dump_smart(
    "🔥 VIVO Y15s V2120 PD2140F - 2 VERSIONS FULL DUMP [UnlockTool]",
    "UnlockTool",
    "dump_model_vivo_y15s_v2120_pd2140f_full_dump_unlocktool",
)
add_dump_smart(
    "🔥 VIVO Y27 & Y36 5G V2248 - PD2279F_EX_A_15.2.10.2.W20 [RARE]",
    "Full Dump [RARE]",
    "dump_model_vivo_y27_y36_5g_v2248_pd2279f_ex_a_15_2_10_2_w20",
)
# The supplied VIVO UnlockTool archive set belongs to the VIVO DUMP catalogue.
# The repeated Y15s PD2140F 6.37.2 link is already represented by the card above.
for _vivo_unlocktool_callback in VIVO_UNLOCKTOOL_DUMP_CALLBACKS:
    _vivo_unlocktool_dump = VIVO_UNLOCKTOOL_DUMPS[_vivo_unlocktool_callback]
    add_dump_smart(
        _vivo_unlocktool_dump["menu"]["en"],
        "UnlockTool",
        _vivo_unlocktool_callback,
    )

add_dump_smart(
    "🔥 SAMSUNG A25 5G SM-A256E - 128GB UFS | 4.5GB [F64 ULTRA]",
    "F64 ULTRA",
    "dump_a256e",
)
add_dump_smart(
    "🔥 M-HORSE POP 8 - 1GB [PANDORA]",
    "Pandora Tool",
    "dump_model_m_horse_pop8",
)
add_dump_smart(
    "🔥 lake POCO C75 / Redmi 14C / REDMI 17C / Redmi A3 Pro - 1GB DUMP",
    "Flash64 Ultra",
    "dump_model_lake_poco_c75_14c_17c",
)

add_dump_smart(
    "🔥 INFINIX HOT 40 Pro - 1GB [M-HORSE]",
    "Pandora Tool",
    "dump_model_infinix_hot40_pro_m_horse",
)

add_dump_smart(
    "🔥 M-HORSE SPARK 10 Pro - 3 VERSIONS FULL DUMP [UnlockTool]",
    "UnlockTool",
    "dump_model_m_horse_spark_10_pro_full_dump_unlocktool",
)


# Link-only ID files: these are not full DUMPs or files stored in this repo.
FREE_ID_FILES = {
    "id_file_brc_an00": {
        "model": "BRC-AN00",
        "version": "9.0.0.150(C00E128R104P1)",
        "url": "https://drive.google.com/file/d/1GjZtvoNMsbyWO7bFGMbJ6YlZmI7H03Ex/view?usp=drive_link",
    },
    "id_file_dvd_an80": {
        "model": "DVD-AN80",
        "version": "9.0.0.148(C00E145R104P5)",
        "url": "https://drive.google.com/file/d/1F3RGTJKD35KwoVLTJ8mKe9PYYQ6NwZ4I/view?usp=drive_link",
    },
    "id_file_lyn_an00": {
        "model": "LYN-AN00",
        "version": "8.0.0.XXX(C00E102R102P3)",
        "url": "https://drive.google.com/file/d/15eolNWKduupEyNi1u3JVJEpRjtFIBjlW/view?usp=drive_link",
        "version_unspecified": True,
    },
    "id_file_noh_an00": {
        "model": "NOH-AN00",
        "version": "2.0.0.222(C00E215R5P6)",
        "url": "https://drive.google.com/file/d/1X7f2LkF0QfSUi4TJ4PscC_XCKWc43CQJ/view?usp=drive_link",
        "os3_only": True,
    },
}

FREE_ID_FILE_LABELS = {
    "ar": {
        "menu_button": "🎁 أربعة ملفات ID مجانية",
        "menu_title": "🎁 أربعة ملفات ID مجانية\n\nاختر الموديل:",
        "model": "الموديل",
        "version": "الإصدار",
        "file": "ملف ID",
        "download": "📥 تحميل ملف ID - Google Drive",
        "back_to_files": "🔙 رجوع إلى ملفات ID",
        "back_to_firmware": "🔙 رجوع إلى الأنظمة",
        "os3_tag": "OS3 فقط",
        "os3_warning": "⚠️ يدعم OS3 فقط.",
        "version_warning": "⚠️ XXX كما ورد في الإصدار المرسل؛ تحقق من رقم الإصدار الفعلي قبل الاستخدام.",
        "check": "⚠️ تحقق من تطابق الموديل والإصدار قبل استخدام الملف.",
    },
    "en": {
        "menu_button": "🎁 Four free ID files",
        "menu_title": "🎁 Four free ID files\n\nSelect a model:",
        "model": "Model",
        "version": "Version",
        "file": "ID file",
        "download": "📥 Download ID file - Google Drive",
        "back_to_files": "🔙 Back to ID files",
        "back_to_firmware": "🔙 Back to firmware",
        "os3_tag": "OS3 only",
        "os3_warning": "⚠️ Supports OS3 only.",
        "version_warning": "⚠️ XXX is the supplied version placeholder; check the exact build before use.",
        "check": "⚠️ Check the model and version match before using this file.",
    },
    "fr": {
        "menu_button": "🎁 Quatre fichiers ID gratuits",
        "menu_title": "🎁 Quatre fichiers ID gratuits\n\nChoisissez un modèle :",
        "model": "Modèle",
        "version": "Version",
        "file": "Fichier ID",
        "download": "📥 Télécharger le fichier ID - Google Drive",
        "back_to_files": "🔙 Retour aux fichiers ID",
        "back_to_firmware": "🔙 Retour aux firmwares",
        "os3_tag": "OS3 uniquement",
        "os3_warning": "⚠️ Compatible avec OS3 uniquement.",
        "version_warning": "⚠️ XXX est indiqué dans la version fournie ; vérifiez la version exacte avant utilisation.",
        "check": "⚠️ Vérifiez que le modèle et la version correspondent avant d'utiliser ce fichier.",
    },
}


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    user_id = call.message.chat.id
    cd = call.data
    hmaxi18n.bind_callback(call.id, user_id)

    if not hmaxx.allow_user(user_id, "callback", is_callback=True, callback_id=call.id):
        return

    # ===== DUMP Tools: card dispatch =====
    try:
        import hmax_dump_tools as _hdt
        _hdt.clear_card_context()
        if str(cd).startswith("dumptoolcard_"):
            short_key = str(cd)[len("dumptoolcard_"):]
            resolved = _hdt.resolve_card_callback(short_key)
            if resolved:
                tool_key, original_cb = resolved
                # ابحث عن label للبطاقة
                card_label = ""
                try:
                    for _lbl, _cb in _hdt.DUMP_CARDS.get(tool_key, []):
                        if _cb == original_cb:
                            card_label = _lbl
                            break
                except Exception:
                    pass
                _hdt.set_card_context(tool_key, original_cb, card_label)
                cd = original_cb
            else:
                try:
                    bot.answer_callback_query(call.id, "⌛ انتهت الجلسة، أعد فتح القائمة.", show_alert=True)
                except Exception:
                    pass
                return
    except Exception as _hdt_err:
        print(f"⚠️ dumptoolcard dispatch: {_hdt_err}")
    # =====================================
    # ===== 💡 كود الإضاءة الجديد - أضفه هنا =====
    if cd == "lighting_status":
        try:
            bot.answer_callback_query(call.id, "💡 ✨ نظام الإضاءة NEON نشط 🟢")
        except:
            pass
        try:
            text = (
                "━━━━━━━━━━━━━━━━━━\n"
                "💡 <b>HMAX LIGHTING SYSTEM</b> 💡\n"
                "━━━━━━━━━━━━━━━━━━\n\n"
                "🟢 <b>الحالة:</b> <code>ONLINE</code>\n"
                "✨ <b>النمط:</b> نيون أزرق #00f0ff\n"
                "🔵 <b>الموقع:</b> مضيء\n"
                "🌟 <b>أزرار البوت:</b> مضيئة\n\n"
                "💡 <b>الميزات:</b>\n"
                "• واجهة ويب مضيئة 🌐\n"
                "• أزرار تيليجرام مضيئة 🤖\n"
                "• شعاع متحرك + LED 🟢\n"
            )
            markup = types.InlineKeyboardMarkup()
            markup.row(types.InlineKeyboardButton("🌐 فتح الموقع المضيء", url="https://hmax-unlocker.onrender.com/light"))
            markup.row(types.InlineKeyboardButton("🔙 رجوع للقائمة المضيئة", callback_data="back_start"))
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="HTML")
        except Exception as e:
            print(f"خطأ الإضاءة: {e}")
        return
    # ===== نهاية كود الإضاءة =====

    # ... باقي الأكواد القديمة حقك تكمل من هنا ...
    # فحص الحظر أولاً لحماية البوت
    if int(user_id) != MY_CHAT_ID and is_user_banned(user_id):
        bot.answer_callback_query(call.id, "🚫 تم حظرك من استخدام البوت.", show_alert=True)
        return

    increment_click()

    # 1. أمر الرد المباشر المطور للأدمن
    if cd.startswith("reply_req_"):
        if int(user_id) != MY_CHAT_ID:
            bot.answer_callback_query(call.id, "❌ هذا الإجراء مخصص للإدارة.", show_alert=True)
            return
        target_id = cd.replace("reply_req_", "").strip()
        if not target_id.isdigit():
            bot.answer_callback_query(call.id, "❌ آيدي المستخدم غير صحيح.", show_alert=True)
            return
        bot.answer_callback_query(call.id)
        msg = bot.send_message(MY_CHAT_ID, f"✍️ **أرسل الآن ردك المباشر للمستخدم صاحب الآيدي (`{target_id}`):**")
        bot.register_next_step_handler(msg, lambda m: send_reply_to_user(m, target_id))
        return

    # 🧩 حل مشكلة تعليق وتجمد زر التحقق من الاشتراك (تمت الإضافة بنجاح هنا)
    elif cd == "check_sub":
        if is_subscribed(user_id, force_refresh=True):
            # إيقاف الدائرة الدوّارة فوراً وإشعار المستخدم بنجاح
            bot.answer_callback_query(call.id, "✅ تم تأكيد الاشتراك بنجاح! أهلاً بك.", show_alert=False)
            try:
                # تنظيف الشات وحذف رسالة الاشتراك الإجباري
                bot.delete_message(user_id, call.message.message_id)
            except:
                pass
            # Continue the start flow after the subscription gate, including the reply keyboard.
            finish_start(user_id, call.from_user.first_name or "", subscription_verified=True)
        else:
            # إذا لم يشترك، أوقف الدائرة واظهر له تنبيه منبثق تحذيري
            bot.answer_callback_query(call.id, "❌ عذراً، أنت غير مشترك في القناة حتى الآن! اشترك أولاً ثم اضغط تحقق.", show_alert=True)
        return


    # 2. ===== قسم اللغة المتصل مرناً مع بقية أزرار وقوائم الملف =====
    elif cd.startswith("set_lang_"):
        lang = cd[len("set_lang_"):]
        if lang not in hmaxi18n.SUPPORTED_LANGUAGES:
            bot.answer_callback_query(call.id, "❌ اللغة غير مدعومة.", show_alert=True)
            return
        saved = hmaxi18n.set_language(user_id, lang)
        bot.answer_callback_query(call.id, "✅ تم تعيين اللغة بنجاح!" if saved else "✅ تم اختيار اللغة لهذه الجلسة.")
        try:
            bot.delete_message(user_id, call.message.message_id)
        except Exception:
            pass
        finish_start(user_id, call.from_user.first_name or "")
        return
            
    elif cd == "change_lang":
        bot.answer_callback_query(call.id)
        try:
            bot.delete_message(user_id, call.message.message_id)
        except Exception:
            pass
        show_language_selection(user_id)
        return


    # ===== 🎯 مركز الخدمات والتفاعل (القسم الشامل المجمع) =====
    elif cd == "community_services_menu":
        try: bot.answer_callback_query(call.id)
        except: pass
        
        markup = types.InlineKeyboardMarkup(row_width=2)
        
        # 1. التسلية والمكافآت
        markup.add(
            types.InlineKeyboardButton("🎡 عجلة الحظ اليومية", callback_data="lucky_spin_menu"),
            types.InlineKeyboardButton("🛒 متجر استبدال النقاط", callback_data="points_store_menu")
        )
        # 2. التشخيص والتنافس
        markup.add(
            types.InlineKeyboardButton("🤖 مساعد التشخيص الذكي", callback_data="gsm_wizard_start"),
            types.InlineKeyboardButton("🏆 لوحة متصدري الدعوات", callback_data="leaderboard_menu")
        )
        # 3. الطلبات والسجلات
        markup.add(
            types.InlineKeyboardButton("📝 طلب أداة", callback_data="req_tool"),
            types.InlineKeyboardButton("📝 سجل تفاعلاتي", callback_data="my_interactions")
        )
        # 4. التقييم والأخبار
        markup.add(
            types.InlineKeyboardButton("⭐ تقييم البوت والخدمة", callback_data="rate_bot_menu"),
            types.InlineKeyboardButton("📢 قناة الأخبار", callback_data="news_channels")
        )
        # 5. زر التواصل المستقل
        markup.row(types.InlineKeyboardButton("💬 تواصل معي خاص", callback_data="main_contact"))
        
        # 6. زر الرجوع
        markup.row(types.InlineKeyboardButton("🏠 العودة للرئيسية", callback_data="back_start"))
        
        display_text = (
            "🎯 **مركز الخدمات والتفاعل الشامل:**\n\n"
            "مرحباً بك في مركز الخدمات! جمعنا لك هنا كل ما تحتاجه للتواصل معنا، طلب الأدوات، تشخيص أعطال الهواتف، واختبار حظك لربح النقاط المجانية.\n\n"
            "💡 **اختر الخدمة المطلوبة من القائمة أدناه:**"
        )
        
        try:
            bot.edit_message_text(
                display_text, call.message.chat.id, call.message.message_id, 
                reply_markup=markup, parse_mode="Markdown"
            )
        except Exception as e:
            print(f"❌ خطأ في فتح مركز الخدمات: {e}")
        return



    # ===== 🛠️ قسم الأدوات (المجمع) =====
    elif cd == "menu_tools_section":
        try: bot.answer_callback_query(call.id)
        except: pass

        lang = hmaxi18n.get_language(user_id)
        flash_tools_labels = {
            "ar": "🛠️ ادوات التفليش الانظمه",
            "en": "🛠️ Flashing & Firmware Tools",
            "fr": "🛠️ Outils de flashage et firmware",
        }
        
        # استخدام صفين وزر في المنتصف لتنسيق أجمل
        markup = types.InlineKeyboardMarkup()
        markup.row(
            types.InlineKeyboardButton("💎 تحديثات الادوات", callback_data="main_tools"),
            types.InlineKeyboardButton("🎁 الادوات المجانيه", callback_data="main_free_tools")
        )
        # 🌟 خيار جديد بزر عريض (صف كامل) لأدوات التفليش والأنظمة
        markup.row(types.InlineKeyboardButton(flash_tools_labels.get(lang, flash_tools_labels["ar"]), callback_data="flash_tools_menu"))
        # 🌟 الزر الجديد تمت إضافته هنا
        markup.row(types.InlineKeyboardButton("🏠 العودة للرئيسية", callback_data="back_start"))
        
        bot.edit_message_text(
            "🛠️ **قسم الأدوات الشامل:**\n\nاختر نوع الأدوات التي تبحث عنها من القائمة أدناه:",
            call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown"
        )
        return

    # ===== 🛠️ ادوات التفليش الانظمه (قسم جديد) =====
    elif cd == "flash_tools_menu":
        try: bot.answer_callback_query(call.id)
        except: pass

        lang = hmaxi18n.get_language(user_id)
        flash_menu_labels = {
            "ar": {
                "title": "🛠️ **ادوات التفليش الانظمه:**\n\nمرحباً بك في قسم أدوات التفليش والأنظمة. اختر الأداة المطلوبة من القائمة أدناه:\n\n💡 جميع الأدوات مجانية ومجربة من طرف الفنيين.",
                "extractor": "📦 Firmware Extractor",
                "unisoc_spd": "📲 تفليش Unisoc-SPD",
                "simunlocker_odin": "🧰 SIMUNLOCKER_ODIN — أداة لتفليش أنظمة السامسونج كاملة أو قطاعات محددة",
                "back": "🔙 رجوع",
            },
            "en": {
                "title": "🛠️ **Flashing and Firmware Tools:**\n\nWelcome to the flashing tools section. Choose the tool you need from the list below:\n\n💡 All tools are free and field-tested.",
                "extractor": "📦 Firmware Extractor",
                "unisoc_spd": "📲 Unisoc-SPD Flashing",
                "simunlocker_odin": "🧰 SIMUNLOCKER_ODIN — Flash full Samsung firmware or selected partitions",
                "back": "🔙 Back",
            },
            "fr": {
                "title": "🛠️ **Outils de flashage et de firmware :**\n\nBienvenue dans la section des outils de flashage. Choisissez l'outil souhaité ci-dessous :\n\n💡 Tous les outils sont gratuits et testés sur le terrain.",
                "extractor": "📦 Firmware Extractor",
                "unisoc_spd": "📲 Flashage Unisoc-SPD",
                "simunlocker_odin": "🧰 SIMUNLOCKER_ODIN — Flasher un firmware Samsung complet ou des partitions choisies",
                "back": "🔙 Retour",
            },
        }
        labels = flash_menu_labels.get(lang, flash_menu_labels["ar"])
        # زر عريض (صف كامل) لفتح صفحة الأداة
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.row(types.InlineKeyboardButton(labels["extractor"], callback_data="flash_fw_extractor"))
        markup.row(types.InlineKeyboardButton(labels["unisoc_spd"], callback_data="flash_unisoc_spd"))
        # 🌟 زر SIMUNLOCKER_ODIN — رابط تحميل مباشر (تفليش أنظمة السامسونج كاملة أو قطاعات محددة)
        markup.row(types.InlineKeyboardButton(
            labels["simunlocker_odin"],
            url="https://www.mediafire.com/file/ji1cgxb398up8lp/SIMUNLOCKER_ODIN1.1-V-1.rar/file",
        ))
        markup.row(types.InlineKeyboardButton(labels["back"], callback_data="menu_tools_section"))
        _hmax_show_menu(call, labels["title"], markup, parse_mode="Markdown")
        return

    # ===== 📱 Firmware Extractor — Dev by Rasheed =====
    elif cd == "flash_fw_extractor":
        try: bot.answer_callback_query(call.id)
        except: pass

        if 'track_tool' in globals():
            track_tool("Firmware Extractor", user_id)

        lang = hmaxi18n.get_language(user_id)
        extractor_labels = {
            "ar": {
                "intro": "🛠️ أداة احترافية تعمل على ويندوز بنقرة واحدة لاستخراج الأقسام (Partitions) من أي فلاشة تقريباً:",
                "download": "⬇️ تحميل FirmwareExtractor.zip",
                "note": "⚠️ ملاحظة: أوقف مضاد الفيروسات مؤقتاً عند فك الضغط حتى لا يحذف ملفات التشغيل الأساسية للأداة.",
                "back": "🔙 رجوع",
            },
            "en": {
                "intro": "🛠️ A professional one-click Windows tool that extracts partitions from almost any firmware:",
                "download": "⬇️ Download FirmwareExtractor.zip",
                "note": "⚠️ Note: temporarily disable your antivirus before extracting the archive so the tool files are not removed.",
                "back": "🔙 Back",
            },
            "fr": {
                "intro": "🛠️ Un outil Windows professionnel qui extrait les partitions de presque n'importe quel firmware en un clic :",
                "download": "⬇️ Télécharger FirmwareExtractor.zip",
                "note": "⚠️ Remarque : désactivez temporairement votre antivirus avant de décompresser l'archive pour ne pas supprimer les fichiers de l'outil.",
                "back": "🔙 Retour",
            },
        }
        labels = extractor_labels.get(lang, extractor_labels["ar"])

        extractor_body = (
            "📱 **Firmware Extractor** — Dev by Rasheed\n\n"
            "A one-click Windows GUI that extracts partitions from almost any firmware:\n\n"
            "• OPPO (.ozip)\n"
            "• Samsung (.tar.md5)\n"
            "• LG (.kdz)\n"
            "• A/B OTAs (payload.bin)\n"
            "• Unisoc (.pac)\n"
            "• QFIL\n"
            "• KDZ\n"
            "• RUU\n"
            "& 22+ formats!\n\n"
            "All-in-one tool, now with a clean GUI. Try it out! 🚀"
        )

        display_text = labels["intro"] + "\n\n" + extractor_body + "\n\n" + labels["note"]

        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.row(types.InlineKeyboardButton(
            labels["download"],
            url="https://drive.google.com/file/d/1WnxIdOCT1hxOWsHHPwBOx6upw_puCcKQ/view",
        ))
        markup.row(types.InlineKeyboardButton(labels["back"], callback_data="flash_tools_menu"))

        _hmax_show_menu(call, display_text, markup, parse_mode="Markdown")
        return

    # ===== 📲 تفليش Unisoc-SPD (Spreadtrum) =====
    elif cd == "flash_unisoc_spd":
        try: bot.answer_callback_query(call.id)
        except: pass

        if 'track_tool' in globals():
            track_tool("Unisoc SPD Flashing Tools", user_id)

        lang = hmaxi18n.get_language(user_id)
        spd_labels = {
            "ar": {
                "title": "📲 **تفليش Unisoc-SPD (Spreadtrum):**\n\n"
                         "الأدوات الرسمية لتفليش أجهزة Unisoc / SPD — اختر الأداة التي تحتاجها من الأزرار أدناه:\n\n"
                         "💡 نصيحة: ثبّت تعاريف SPD على الكمبيوتر قبل البدء لضمان اتصال مستقر أثناء العملية.",
                "upgrade": "⬇️ SPD Upgrade Tool R27.25.4601",
                "research": "⬇️ SPD Research Tool R27.24.2301",
                "factory": "⬇️ SPD Factory Tool R27.25.4601",
                "back": "🔙 رجوع",
            },
            "en": {
                "title": "📲 **Unisoc-SPD Flashing (Spreadtrum):**\n\n"
                         "Official flashing tools for Unisoc / SPD devices — pick the tool you need from the buttons below:\n\n"
                         "💡 Tip: install the SPD drivers on your PC first for a stable connection during the process.",
                "upgrade": "⬇️ SPD Upgrade Tool R27.25.4601",
                "research": "⬇️ SPD Research Tool R27.24.2301",
                "factory": "⬇️ SPD Factory Tool R27.25.4601",
                "back": "🔙 Back",
            },
            "fr": {
                "title": "📲 **Flashage Unisoc-SPD (Spreadtrum) :**\n\n"
                         "Outils de flashage officiels pour les appareils Unisoc / SPD — choisissez l'outil souhaité ci-dessous :\n\n"
                         "💡 Astuce : installez d'abord les pilotes SPD sur le PC pour une connexion stable pendant l'opération.",
                "upgrade": "⬇️ SPD Upgrade Tool R27.25.4601",
                "research": "⬇️ SPD Research Tool R27.24.2301",
                "factory": "⬇️ SPD Factory Tool R27.25.4601",
                "back": "🔙 Retour",
            },
        }
        labels = spd_labels.get(lang, spd_labels["ar"])

        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.row(types.InlineKeyboardButton(labels["upgrade"], url="https://www.mediafire.com/file/17wygio8opba6na/SPD_Upgrade_Tool_R27.25.4601.zip/file"))
        markup.row(types.InlineKeyboardButton(labels["research"], url="https://www.mediafire.com/file/67lq7q43s7m56wz/SPD_Research_Tool_R27.24.2301.zip/file"))
        markup.row(types.InlineKeyboardButton(labels["factory"], url="https://www.mediafire.com/file/rtoistsbxqttyr5/SPD_Factory_Tool_R27.25.4601.zip/file"))
        markup.row(types.InlineKeyboardButton(labels["back"], callback_data="flash_tools_menu"))

        _hmax_show_menu(call, labels["title"], markup, parse_mode="Markdown")
        return

       # ===== 📥 قسم الأنظمة (المجمع) =====
    elif cd == "menu_systems_section":
        try: bot.answer_callback_query(call.id)
        except: pass

        lang = hmaxi18n.get_language(user_id)
        f64_button_labels = {
            "ar": "🛠️ دامب عبر جيتاج F64 ULTRA",
            "en": "🛠️ DUMP via F64 ULTRA JTAG",
            "fr": "🛠️ DUMP via JTAG F64 ULTRA",
        }
        dump_tools_btn_labels = {
            "ar": "🛠️ أدوات سحب الدامب",
            "en": "🛠️ DUMP Flashing Tools",
            "fr": "🛠️ Outils de flashage DUMP",
        }
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🌐 مواقع الأنظمة جميع الشركات مجانا", callback_data="main_firmware_sites"),
            types.InlineKeyboardButton("📂 انظمه نادره مجانا", callback_data="rare_free_list"),
            types.InlineKeyboardButton(
                FREE_ID_FILE_LABELS.get(lang, FREE_ID_FILE_LABELS["ar"])["menu_button"],
                callback_data="id_files_section",
            ),
            types.InlineKeyboardButton("💾 قسم ملفات الـ DUMP", callback_data="dump_main_section"),
            types.InlineKeyboardButton(f64_button_labels.get(lang, f64_button_labels["ar"]), callback_data="f64_ultra_dump_section"),
            types.InlineKeyboardButton(dump_tools_btn_labels.get(lang, dump_tools_btn_labels["ar"]), callback_data="dump_tools_section"),
            types.InlineKeyboardButton("🏠 العودة للرئيسية", callback_data="back_start")
        )
        
        _hmax_show_menu(
            call,
            "📥 **مستودع الأنظمة (Firmwares):**\n\nاختر القسم المطلوب لتحميل الفلاشات والرومات الرسمية أدناه:",
            markup,
            parse_mode="Markdown",
        )
        return

    elif cd == "id_files_section":
        lang = hmaxi18n.get_language(user_id)
        labels = FREE_ID_FILE_LABELS.get(lang, FREE_ID_FILE_LABELS["ar"])
        markup = types.InlineKeyboardMarkup(row_width=1)
        for callback, entry in FREE_ID_FILES.items():
            title = f"📱 {entry['model']} {entry['version']}"
            if entry.get("os3_only"):
                title += f" ({labels['os3_tag']})"
            markup.add(types.InlineKeyboardButton(title, callback_data=callback))
        markup.add(types.InlineKeyboardButton(
            labels["back_to_firmware"], callback_data="menu_systems_section",
        ))
        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass
        _hmax_show_menu(call, labels["menu_title"], markup)
        return

    elif cd in FREE_ID_FILES:
        lang = hmaxi18n.get_language(user_id)
        labels = FREE_ID_FILE_LABELS.get(lang, FREE_ID_FILE_LABELS["ar"])
        entry = FREE_ID_FILES[cd]
        details = [
            f"📁 {labels['file']}",
            "━━━━━━━━━━━━",
            f"📱 {labels['model']}: {entry['model']}",
            f"🔢 {labels['version']}: {entry['version']}",
        ]
        if entry.get("os3_only"):
            details.append(labels["os3_warning"])
        if entry.get("version_unspecified"):
            details.append(labels["version_warning"])
        details.extend(("━━━━━━━━━━━━", labels["check"]))
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton(labels["download"], url=entry["url"]))
        markup.add(types.InlineKeyboardButton(
            labels["back_to_files"], callback_data="id_files_section",
        ))
        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass
        _hmax_show_menu(call, "\n".join(details), markup)
        return

    elif cd == "dump_tools_section":
        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass
        try:
            import hmax_dump_tools
            lang = hmaxi18n.get_language(user_id)
            hmax_dump_tools._show_main(call.message.chat.id, call.message.message_id, lang)
        except Exception as e:
            print(f"❌ dump_tools_section: {e}")
        return

    elif cd == "dumpadv_recent":
        try:
            import hmax_dump_advanced as _adv
            lang = hmaxi18n.get_language(user_id)
            _adv.show_recent(call, lang)
        except Exception as e:
            print(f"❌ dumpadv_recent: {e}")
        return

    elif cd == "dumpadv_favorites":
        try:
            import hmax_dump_advanced as _adv
            lang = hmaxi18n.get_language(user_id)
            _adv.show_favorites(call, lang)
        except Exception as e:
            print(f"❌ dumpadv_favorites: {e}")
        return

    elif cd == "dumpadv_search":
        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass
        msg = bot.send_message(
            user_id,
            "🔍 أرسل كلمة البحث عن البطاقة (أو اكتب 'إلغاء'):",
        )
        bot.register_next_step_handler(msg, _handle_dump_search)
        return

    elif str(cd).startswith("dumpfav_"):
        try:
            import hmax_dump_advanced as _adv
            from hmax_dump_tools import DUMP_CARDS
            token = str(cd)[len("dumpfav_"):]
            original_cb = _adv._resolve_fav_token(token)
            if not original_cb:
                bot.answer_callback_query(call.id, "⌛ انتهت الجلسة، أعد فتح البطاقة.", show_alert=True)
                return
            card_label = original_cb
            for _tk, _cards in DUMP_CARDS.items():
                for _lbl, _cb in _cards:
                    if _cb == original_cb:
                        card_label = _lbl
                        break
            added, err = _adv.toggle_favorite(user_id, original_cb, card_label)
            if err:
                bot.answer_callback_query(call.id, f"❌ {err}", show_alert=True)
                return
            if added:
                bot.answer_callback_query(call.id, "⭐ تم الحفظ في المفضلة", show_alert=False)
            else:
                bot.answer_callback_query(call.id, "🗑️ تم الإزالة من المفضلة", show_alert=False)
        except Exception as e:
            print(f"❌ dumpfav_: {e}")
            try:
                bot.answer_callback_query(call.id, "❌ حدث خطأ", show_alert=True)
            except Exception:
                pass
        return

    elif cd == "admin_dump_health":
        if int(user_id) != MY_CHAT_ID:
            bot.answer_callback_query(call.id, "❌ للإدارة فقط", show_alert=True)
            return
        try:
            import hmax_dump_advanced as _adv
            lang = hmaxi18n.get_language(user_id)
            _adv.show_library_health(call, lang)
        except Exception as e:
            print(f"❌ admin_dump_health: {e}")
        return

    elif cd == "dump_tools_jtag":
        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass
        try:
            import hmax_dump_tools
            lang = hmaxi18n.get_language(user_id)
            hmax_dump_tools._show_category(call.message.chat.id, call.message.message_id, "jtag", lang)
        except Exception as e:
            print(f"❌ dump_tools_jtag: {e}")
        return

    elif cd == "dump_tools_normal":
        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass
        try:
            import hmax_dump_tools
            lang = hmaxi18n.get_language(user_id)
            hmax_dump_tools._show_category(call.message.chat.id, call.message.message_id, "normal", lang)
        except Exception as e:
            print(f"❌ dump_tools_normal: {e}")
        return
    elif str(cd).startswith("dumptoolinfo_"):
        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass
        try:
            import hmax_dump_tools
            lang = hmaxi18n.get_language(user_id)
            hmax_dump_tools._show_tool_info(call, str(cd)[len("dumptoolinfo_"):], lang)
        except Exception as e:
            print(f"❌ dumptoolinfo_: {e}")
        return

    elif str(cd).startswith("dumptool_"):
        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass
        try:
            import hmax_dump_tools
            lang = hmaxi18n.get_language(user_id)
            hmax_dump_tools._show_tool_cards(call, str(cd)[len("dumptool_"):], lang)
        except Exception as e:
            print(f"❌ dumptool_: {e}")
        return

    elif cd == "f64_ultra_dump_section":
        lang = hmaxi18n.get_language(user_id)
        translations = {
            "ar": {
                "title": "🛠️ DUMP عبر جيتاج F64 ULTRA",
                "redmi": "📱 ريدمي F64",
                "all": "📁 كل دامبات F64",
                "back": "🔙 رجوع",
            },
            "en": {
                "title": "🛠️ DUMP via F64 ULTRA JTAG",
                "redmi": "📱 Redmi F64",
                "all": "📁 All F64 DUMPs",
                "back": "🔙 Back",
            },
            "fr": {
                "title": "🛠️ DUMP via JTAG F64 ULTRA",
                "redmi": "📱 Redmi F64",
                "all": "📁 Tous les DUMP F64",
                "back": "🔙 Retour",
            },
        }
        labels = translations.get(lang, translations["ar"])
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton(labels["redmi"], callback_data="f64_redmi_section"),
            types.InlineKeyboardButton(labels["all"], callback_data="f64_all_section"),
            # The F64 menu is opened from the systems repository, so back
            # must return there instead of jumping into the brand menu.
            types.InlineKeyboardButton(labels["back"], callback_data="menu_systems_section"),
        )
        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass
        _hmax_show_menu(call, labels["title"], markup)
        return

    elif cd in ("f64_redmi_section", "f64_all_section"):
        lang = hmaxi18n.get_language(user_id)
        translations = {
            "ar": {
                "title": "📁 دامبات ريدمي F64" if cd == "f64_redmi_section" else "📁 كل دامبات F64",
                "model": "📱 REDMI 10A 220233L2G - 64GB",
                "poco": "📱 POCO C65 - 256GB [F64 ULTRA]",
                "back": "🔙 رجوع",
            },
            "en": {
                "title": "📁 Redmi F64 DUMPs" if cd == "f64_redmi_section" else "📁 All F64 DUMPs",
                "model": "📱 REDMI 10A 220233L2G - 64GB",
                "poco": "📱 POCO C65 - 256GB [F64 ULTRA]",
                "back": "🔙 Back",
            },
            "fr": {
                "title": "📁 DUMP Redmi F64" if cd == "f64_redmi_section" else "📁 Tous les DUMP F64",
                "model": "📱 REDMI 10A 220233L2G - 64GB",
                "poco": "📱 POCO C65 - 256GB [F64 ULTRA]",
                "back": "🔙 Retour",
            },
        }
        labels = translations.get(lang, translations["ar"])
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton(
            labels["model"],
            callback_data="dump_model_redmi_10a_220233l2g",
        ))
        markup.add(types.InlineKeyboardButton(
            labels["poco"],
            callback_data="dump_model_poco_c65_256gb",
        ))
        # These lists are opened from the F64 ULTRA menu, so back returns
        # there instead of skipping all the way to the systems repository.
        markup.add(types.InlineKeyboardButton(labels["back"], callback_data="f64_ultra_dump_section"))
        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass
        _hmax_show_menu(call, labels["title"], markup)
        return

    # ===== 💾 قسم الـ DUMP =====
    elif cd == "dump_main_section":
        lang = hmaxi18n.get_language(user_id)
        translations = {
            "ar": {
                "title": "🗄️ *HMAX DUMP LIBRARY*\n📚 تصفح الملفات حسب الماركة\n━━━━━━━━━━━━\nاختر الماركة لعرض ملفاتها",
                "allcall": "📱 ALLCALL MAGIC",
                "hmd": "📱 HMD",
                "honor": "🗄️ HUAWEI & HONOR",
                "nokia": "📱 NOKIA",
                "infinix": "📱 INFINIX",
                "itel": "📱 ITEL",
                "m_horse": "📱 M-HORSE",
                "oppo": "📱 OPPO",
                "realme": "📱 REALME",
                "samsung_scatter": "📁 DUMP + Scatter Samsung",
                "xiaomi": "📱 XIAOMI | REDMI | POCO",
                "tecno": "📱 TECNO",
                "vivo": "📱 VIVO",
                "zte": "🗄️ ZTE",
                "copy": "💾 COPY",
                "iphone_copy": "🍎 iPhone Copy",
                "other": "💿 OTHER",
                "back": "🔙 رجوع",
            },
            "en": {
                "title": "🗄️ *HMAX DUMP LIBRARY*\n📚 Browse files by brand\n━━━━━━━━━━━━\nSelect a brand to view its files",
                "allcall": "📱 ALLCALL MAGIC",
                "hmd": "📱 HMD",
                "honor": "🗄️ HUAWEI & HONOR",
                "nokia": "📱 NOKIA",
                "infinix": "📱 INFINIX",
                "itel": "📱 ITEL",
                "m_horse": "📱 M-HORSE",
                "oppo": "📱 OPPO",
                "realme": "📱 REALME",
                "samsung_scatter": "📁 DUMP + Scatter Samsung",
                "xiaomi": "📱 XIAOMI | REDMI | POCO",
                "tecno": "📱 TECNO",
                "vivo": "📱 VIVO",
                "zte": "🗄️ ZTE",
                "copy": "💾 COPY",
                "iphone_copy": "🍎 iPhone Copy",
                "other": "💿 OTHER",
                "back": "🔙 Back",
            },
            "fr": {
                "title": "🗄️ *Bibliothèque HMAX DUMP*\n📚 Parcourez les fichiers par marque\n━━━━━━━━━━━━\nChoisissez une marque pour voir ses fichiers",
                "allcall": "📱 ALLCALL MAGIC",
                "hmd": "📱 HMD",
                "honor": "🗄️ HUAWEI & HONOR",
                "nokia": "📱 NOKIA",
                "infinix": "📱 INFINIX",
                "itel": "📱 ITEL",
                "m_horse": "📱 M-HORSE",
                "oppo": "📱 OPPO",
                "realme": "📱 REALME",
                "samsung_scatter": "📁 DUMP + Scatter Samsung",
                "xiaomi": "📱 XIAOMI | REDMI | POCO",
                "tecno": "📱 TECNO",
                "vivo": "📱 VIVO",
                "zte": "🗄️ ZTE",
                "copy": "💾 COPY",
                "iphone_copy": "🍎 iPhone Copy",
                "other": "💿 OTHER",
                "back": "🔙 Retour",
            },
        }
        labels = translations.get(lang, translations["ar"])
        markup = types.InlineKeyboardMarkup(row_width=1)
        txt = labels["title"]

        markup.add(types.InlineKeyboardButton(labels["allcall"], callback_data="dump_allcall_magic_section"))
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📱 AllCall"), callback_data="dump_allcall_section"))  # <-- القسم الجديد
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📱 KXD A07 - Dual Versions"), callback_data="dump_kxd_section"))
        markup.add(types.InlineKeyboardButton(labels["hmd"], callback_data="dump_hmd_section"))
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📱 BENCO"), callback_data="dump_benco_section"))
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📱 HONOR"), callback_data="dump_honor_section"))
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📱 HISORL"), callback_data="dump_hisorl_section"))
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📱 BLACKVIEW"), callback_data="dump_blackview_section"))
        markup.add(types.InlineKeyboardButton(labels["honor"], callback_data="dump_huawei_section"))
        markup.add(types.InlineKeyboardButton(labels["nokia"], callback_data="dump_nokia_section"))
        markup.add(types.InlineKeyboardButton(labels["infinix"], callback_data="dump_infinix_full_section"))
        markup.add(types.InlineKeyboardButton(labels["itel"], callback_data="dump_itel_full_section"))
        markup.add(types.InlineKeyboardButton(labels["m_horse"], callback_data="dump_m_horse_section"))
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📱 OPPO"), callback_data="dump_oppo_section"))
        markup.add(types.InlineKeyboardButton(labels["realme"], callback_data="dump_realme_section"))
        markup.add(types.InlineKeyboardButton(labels["samsung_scatter"], callback_data="dump_scatter_samsung"))
        markup.add(types.InlineKeyboardButton(
            labels["xiaomi"],
            callback_data="dump_xiaomi_group_section",
        ))
        markup.add(types.InlineKeyboardButton(labels["tecno"], callback_data="dump_tecno_full_section"))
        markup.add(types.InlineKeyboardButton(labels["vivo"], callback_data="dump_vivo_full_section"))
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📱 WIKO"), callback_data="dump_wiko_section"))
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📱 VILLAON"), callback_data="dump_villaon_section"))
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📱 TAB"), callback_data="dump_tab_section"))
        markup.add(types.InlineKeyboardButton(labels["zte"], callback_data="dump_zte_full_section"))
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📱 Motorola"), callback_data="dump_motorola_section"))
        markup.add(types.InlineKeyboardButton(labels["copy"], callback_data="dump_copy_full_section"))
        markup.add(types.InlineKeyboardButton(
            labels["iphone_copy"],
            callback_data="dump_iphone_copy_section",
        ))
        markup.add(types.InlineKeyboardButton(labels["other"], callback_data="dump_other_full_section"))
        markup.add(types.InlineKeyboardButton(labels["back"], callback_data="menu_systems_section"))

        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass
        _hmax_show_menu(call, txt, markup, parse_mode="Markdown")
        return

    elif cd == "dump_benco_section":
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "🔥 V60 Full Dump [CM2]"), callback_data="dump_model_benco_v60_full"))
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "🔥 S1 Pro AE9260 Dual Dump [PANDORA + CM2]"), callback_data="dump_model_benco_s1_pro_ae9260_dual"))
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "⬅️ Back to DUMP"), callback_data="dump_main_section"))
        section_text = (
            "📱 BENCO - Official Firmware Library\n"
            "━━━━━━━━━━━━\n"
            "🔷 Brand: BENCO\n"
            "📦 Full Dump Library\n"
            "☁️ Google Drive\n"
            "━━━━━━━━━━━━\n"
            "اختر الموديل:"
        )
        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass
        _hmax_show_menu(call, _dump_localize(user_id, section_text), markup)
        return

    elif cd in ("dump_honor_section", "dump_honor_full_section"):
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "🔥 HONOR 70 FNE-NX9 - Official FREE"), callback_data="dump_model_fne_nx9_official"))
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "🔥 X7a RKY-LX2 2GB DUMP [F64 Ultra]"), callback_data="dump_model_honor_x7a_rky_lx2_2gb"))
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "⭐ X9c FULL DUMP [Flash64 Ultra]"), callback_data="dump_model_honor_x9c_full_dump"))
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "🔥 X7b 5G CLK-NX2 FRP [YMTC]"), callback_data="dump_model_honor_x7b_5g_frp"))
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "🗄️ HUAWEI & HONOR Library"), callback_data="dump_huawei_honor_section"))
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "⬅️ Back to DUMP"), callback_data="dump_main_section"))
        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass
        _hmax_show_menu(call, _dump_localize(user_id, "📱 HONOR - Firmware Library\n━━━━━━━━━━━━\n🔷 Brand: HONOR\n📦 FULL DUMP\n━━━━━━━━━━━━\nاختر الموديل:"), markup)
        return

    elif cd == "dump_model_fne_nx9_official":
        markup = types.InlineKeyboardMarkup(row_width=1)
        gdrive_url = "https://drive.google.com/file/d/1sPDlg3-8j4OiL12Zh1DZNHF4Y5mHNjJd/view"
        photo_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "images",
            "honor_70_fne-nx9_official_hmax.jpg",
        )
        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass
        try:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except Exception:
            pass
        txt = (
            "🔥 HONOR 70 — FNE-NX9 — Official Firmware 🔥\n"
            "━━━━━━━━━━━━\n"
            "💎 الفلاشة الرسمية المدفوعة — متاحة الآن مجاناً\n"
            "━━━━━━━━━━━━\n"
            "📦 بيانات الفلاشة:\n"
            "• Model: HONOR 70 5G\n"
            "• Variant: FNE-NX9\n"
            "• Firmware: FNE-N29_def_meafnaf_8.0.0.292_C185E7R2P1\n"
            "• MagicOS: 8.0_0501AAEM\n"
            "• Hosting: Google Drive\n"
            "• Password: MobiFirmware.VIP\n"
            "━━━━━━━━━━━━\n"
            "📱 المواصفات:\n"
            "• 6.67 OLED 120Hz - Snapdragon 778G+ 5G\n"
            "• 8GB/12GB - 128/256/512GB\n"
            "• 54+50+2MP - 32MP - 4800mAh 66W\n"
            "━━━━━━━━━━━━\n"
            "HMAX-UNLOCKER - HithamMax\n"
        )
        txt = _dump_card_text(user_id, "dump_model_fne_nx9_official", txt)
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📥 Download"), url=gdrive_url))
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "⬅️ Back to HONOR"), callback_data="dump_honor_section"))
        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(call.message.chat.id, photo, caption=txt, reply_markup=markup)
        except Exception:
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    elif cd == "dump_model_benco_s1_pro_ae9260_dual":
        markup = types.InlineKeyboardMarkup(row_width=2)
        photo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", "benco_s1_pro_ae9260_dual_dump.jpg")
        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass
        try:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except Exception:
            pass
        txt = (
            "⭐ BENCO S1 Pro — AE9260 — DUAL FULL DUMP 🔥\n"
            "━━━━━━━━━━━━\n"
            "📁 وفرنا أكتر من خيار للدامب علشان الفني يلاقي الحل المناسب\n"
            "━━━━━━━━━━━━\n"
            "📁 Dump 1 | Pandora Tool:\n"
            "Benco S1 Pro AE9260 - S174-24F25 Lava Dump By Pandora\n"
            "━━━━━━━━━━━━\n"
            "📁 Dump 2 | CM2:\n"
            "BENCO_S1_PRO_UMS9230_INONE_AE9260_OSv13_benco_AE9260_S174_24F25 FULL DUMP BY CM2\n"
            "━━━━━━━━━━━━\n"
            "🔧 Tools: Pandora Tool + CM2\n"
            "🔐 Pass: MobiFirmware.VIP\n"
            "💡 Feature: اختيارات متعددة لنفس الجهاز = مرونة أكبر\n"
        )
        txt = _dump_card_text(user_id, "dump_model_benco_s1_pro_ae9260_dual", txt)
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📥 Dump 1 - Pandora"), url="https://drive.google.com/file/d/1Dx6I5z92KofjEru4xveT7SZ-TeQj7a_L/view"))
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📥 Dump 2 - CM2"), url="https://drive.google.com/file/d/19xbfXJYSKw-PN1d6QBrscmOFwqqoKDjY/view"))
        markup.add(types.InlineKeyboardButton(_dump_back_label(user_id, "⬅️ Back"), callback_data="dump_benco_section"))
        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(call.message.chat.id, photo, caption=txt, reply_markup=markup)
        except Exception:
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    elif cd == "dump_model_honor_x7a_rky_lx2_2gb":
        markup = types.InlineKeyboardMarkup(row_width=1)
        photo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", "honor_x7a_rky_lx2_2gb_dump_f64.jpg")
        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass
        try:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except Exception:
            pass
        txt = (
            "⭐ HONOR X7a — RKY-LX2 — 2GB DUMP 🔥\n"
            "━━━━━━━━━━━━\n"
            "📁 File: 2GB DUMP | شامل ملفات الشبكة\n"
            "⚡ Pulled By: F64 Ultra\n"
            "📤 Shared By: Hossam Khairy\n"
            "🙏 Thanks: ساحر F64 Ultra - Hossam Khairy\n"
            "━━━━━━━━━━━━\n"
            "📱 Device: HONOR X7a RKY-LX2\n"
            "📦 Size: 2GB DUMP | Network Files Included\n"
            "🔧 Tool: F64 Ultra\n"
            "☁️ Hosting: Google Drive\n"
            "🔐 Pass: MobiFirmware.VIP\n"
        )
        txt = _dump_card_text(user_id, "dump_model_honor_x7a_rky_lx2_2gb", txt)
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📥 Download - Google Drive"), url="https://drive.google.com/file/d/1TiQ4y7sUK6cNxaUVT2tEcjgC3vjdlEr0/view"))
        markup.add(types.InlineKeyboardButton(_dump_back_label(user_id, "⬅️ Back"), callback_data="dump_honor_section"))
        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(call.message.chat.id, photo, caption=txt, reply_markup=markup)
        except Exception:
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    elif cd == "dump_model_honor_x9c_full_dump":
        markup = types.InlineKeyboardMarkup(row_width=1)
        gdrive_url = "https://drive.google.com/file/d/1Kd5cp_IQeTI_6fzz0HmZVgHKT-DSZfL0/view"
        photo_path = "images/honor_x9c_full_dump.jpg"
        try:
            bot.answer_callback_query(call.id)
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except: pass
        txt = (
            "⭐ HONOR X9c — FULL DUMP 🔥\n"
            "تم رفع الدامب بالكامل على Google Drive بناءً على احتياج الفنيين، لتوفير ملف جاهز للاستخدام في عمليات السوفت وير والبرمجة. 💛🔥\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "📱 مواصفات الهاتف:\n"
            "🔹 Model: 【entity-HONOR¦canonical_name=HONOR】 X9c\n"
            "🔹 Processor: 【entity-Qualcomm¦canonical_name=Qualcomm】 【entity-Snapdragon¦canonical_name=Snapdragon】 6 Gen 1\n"
            "🔹 Display: 6.78\" AMOLED\n"
            "🔹 Resolution: 2700 × 1224 — 1.5K\n"
            "🔹 Refresh Rate: 120Hz\n"
            "🔹 Main Camera: 108MP + OIS\n"
            "🔹 Battery: 6600mAh\n"
            "🔹 Charging: 66W 【entity-HONOR¦canonical_name=HONOR】 SuperCharge\n"
            "🔹 OS: MagicOS 8.0 — Android 14\n"
            "🔹 Network: 5G / 4G LTE\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "📁 بيانات الملف:\n"
            "Device: 【entity-HONOR¦canonical_name=HONOR】 X9c\n"
            "File: FULL DUMP\n"
            "Pulled By: Flash64 Ultra\n"
            "Upload: Google Drive\n"
            "Pass File: MobiFirmware.VIP\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "HMAX hithamMax - PROFESSIONAL FIRMWARE SOLUTIONS\n"
        )
        txt = _dump_card_text(user_id, "dump_model_honor_x9c_full_dump", txt)
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📥 Download - Google Drive"), url=gdrive_url))
        markup.add(types.InlineKeyboardButton(_dump_back_label(user_id, "⬅️ Back"), callback_data="dump_honor_section"))
        try:
            with open(photo_path, 'rb') as photo:
                bot.send_photo(call.message.chat.id, photo, caption=txt, reply_markup=markup)
        except Exception as e:
            print(f"Photo error: {e}")
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)

    elif cd == "dump_model_honor_x7b_5g_frp":
        lang = hmaxi18n.get_language(user_id)
        photo_path = "images/honor_x7b_5g_clk_nx2_frp_ymtc_hmax.jpg"
        emmc_url = "https://www.mediafire.com/file/oqlqu315m5kutkh/Z3x+Emmc+Manager-1.23-26-11-2023+Upload+by+Aftab+Ansari+(Team+-+www.Martview-Forum.com).rar/file"
        try:
            bot.answer_callback_query(call.id)
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except: pass

        txts = {
            "ar": (
                "🔥 【entity-HONOR¦canonical_name=HONOR】 X7b 5G - CLK-NX2 - FRP SUCCESS 🔥\n"
                "━━━━━━━━━━━━\n"
                "📱 Model: 【entity-HONOR¦canonical_name=HONOR】 X7b 5G CLK-NX2\n"
                "🧠 Chip: Dimensity 6020\n"
                "💾 RAM: 8GB+8GB Turbo\n"
                "🔋 Battery: 6000mAh\n"
                "📱 Resolution: 2412x1080\n"
                "💿 Storage: 256GB\n"
                "🔖 Build: MagicOS 9.0.0.164(C185E5R2P2) Android 15 GPU Turbo\n"
                "🧩 Memory: YMTC\n"
                "━━━━━━━━━━━━\n"
                "💎 نختم اليوم بجهاز حقير x7b الجهاز مش قابل بوكسات سيف علي كدا ذاكرة من نوع ymtc\n"
                "الذواكر دي لو انت شغال علي الايزي جيتاج مش حتقرا معاك غير علي emmc manager tool لان البوكس مش داعمها\n"
                "━━━━━━━━━━━━\n"
                "❌ المشكلة 1: emmc manager بتجيب box not detected\n"
                "✅ الحل: نسخة Z3x Emmc Manager 1.23-26-11-2023\n"
                "🔑 Pass: martviewforum\n"
                "❌ المشكلة 2: لما تعمل reset frp البرنامج مش بيتعرف علي بارتيشن frp\n"
                "✅ الحل: browse وسحبت نسخه من frp احتياط ثم erase frp partition وتم بنجاح الحمدلله\n"
                "━━━━━━━━━━━━\n"
                "✅ الحمدلله تم FRP\n"
                "HMAX-UNLOCKER - HithamMax"
            ),
            "en": (
                "🔥 【entity-HONOR¦canonical_name=HONOR】 X7b 5G - CLK-NX2 FRP DONE 🔥\n"
                "📱 CLK-NX2 Dimensity 6020 8+8GB 256GB 6000mAh MagicOS 9.0 Android 15\n"
                "🧩 YMTC memory - Only readable via EMMC Manager Tool, not normal Easy Jtag\n"
                "Issue1: Box Not Detected -> Fix: EMMC Manager 1.23 26-11-2023 Pass: martviewforum\n"
                "Issue2: FRP partition not detected -> Fix: Browse Backup FRP then Erase FRP Partition - Success\n"
                "HMAX-UNLOCKER"
            ),
            "fr": (
                "🔥 【entity-HONOR¦canonical_name=HONOR】 X7b 5G - CLK-NX2 FRP SUCCESS 🔥\n"
                "📱 CLK-NX2 Dimensity 6020 8+8GB 256GB 6000mAh MagicOS 9.0\n"
                "🧩 Mémoire YMTC - lisible uniquement via EMMC Manager Tool\n"
                "Problème1: Box Not Detected -> Solution: EMMC Manager 1.23 Pass: martviewforum\n"
                "Problème2: Partition FRP non détectée -> Sauvegarde FRP puis Erase FRP - Succès\n"
                "HMAX-UNLOCKER"
            ),
        }
        txt = txts.get(lang, txts["ar"])
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton("📥 EMMC Manager 1.23 - Pass: martviewforum", url=emmc_url))
        markup.add(types.InlineKeyboardButton("⬅️ رجوع لـ HONOR", callback_data="dump_honor_full_section"))
        try:
            with open(photo_path,'rb') as p: bot.send_photo(call.message.chat.id, p, caption=txt, reply_markup=markup)
        except: bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    elif cd == "dump_model_nokia_ta_1114_copy":
        markup = types.InlineKeyboardMarkup(row_width=1)
        photo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", "nokia_ta_1114_copy_spreadtrum_miracle.jpg")
        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass
        try:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except Exception:
            pass
        txt = (
            "⭐ NOKIA TA-1114 — COPY VERSION — FLASH FILE 🔥\n"
            "━━━━━━━━━━━━\n"
            "📱 Device: NOKIA TA-1114\n"
            "🔖 Version: COPY VERSION\n"
            "💾 CPU: SPREADTRUM\n"
            "⚡ Pulled By: Miracle Box\n"
            "📤 Upload By: Ahmed ClaSsic\n"
            "━━━━━━━━━━━━\n"
            "☁️ Hosting: Google Drive\n"
            "✅ Status: FLASH FILE READY\n"
        )
        txt = _dump_card_text(user_id, "dump_model_nokia_ta_1114_copy", txt)
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📥 Download - Google Drive"), url="https://drive.usercontent.google.com/download?id=1_c708OPmAWhZW6Fudrl7TCXRkyyU_Scb"))
        markup.add(types.InlineKeyboardButton(_dump_back_label(user_id, "⬅️ Back"), callback_data="dump_nokia_section"))
        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(call.message.chat.id, photo, caption=txt, reply_markup=markup)
        except Exception:
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    elif cd == "dump_hisorl_section":
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "🔥 T901 Full Dump [UnlockTool]"), callback_data="dump_model_hisorl_t901_full"))
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "⬅️ Back to DUMP"), callback_data="dump_main_section"))
        section_text = (
            "📱 HISORL - Official Firmware Library\n"
            "━━━━━━━━━━━━\n"
            "🔷 Brand: HISORL\n"
            "📦 Full Dump Library\n"
            "☁️ Google Drive\n"
            "━━━━━━━━━━━━\n"
            "اختر الموديل:"
        )
        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass
        _hmax_show_menu(call, _dump_localize(user_id, section_text), markup)
        return

    # ===== 📱 BLACKVIEW =====
    elif cd == "dump_blackview_section":
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📱 blackview_a55"), callback_data="dump_blackview_a55"))
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "⬅️ Back to DUMP"), callback_data="dump_main_section"))
        section_text = (
            "📱 BLACKVIEW - Firmware Library\n"
            "━━━━━━━━━━━━\n"
            "🔷 Brand: BLACKVIEW\n"
            "📦 Full Dump Library\n"
            "☁️ Google Drive\n"
            "━━━━━━━━━━━━\n"
            "اختر الموديل:"
        )
        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass
        _hmax_show_menu(call, _dump_localize(user_id, section_text), markup)
        return

    elif cd == "dump_blackview_a55":
        lang = hmaxi18n.get_language(user_id)
        gdrive_url = "https://drive.google.com/file/d/18xsJ8qLtParycTU0qx6KcGO1eabb5Rws/view"
        photo_path = "images/blackview_a55_hmax.jpg"
        try:
            bot.answer_callback_query(call.id)
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except:
            pass

        t = {
            "ar": (
                "🔥 Blackview A55 – Dump Full | UnlockTool 🔥\n"
                "━━━━━━━━━━━━\n"
                "📱 دامب هاتف Blackview A55 تم سحبه بواسطة UnlockTool، وكان مرفوع سابقا على TeraBox ومدفوع.\n"
                "وبناء على طلب الإخوة، تم إعادة رفعه على Google Drive وأصبح الآن:\n"
                "🟢 المدفوع الآن مجاناً 🟢\n"
                "━━━━━━━━━━━━\n"
                "📦 معلومات الدامب:\n"
                "🔹 Brand: Blackview\n🔹 Model: A55\n🔹 CPU: MediaTek MT6761\n"
                "🔹 Android: 11\n🔹 Build Number: A55_V1.0_20250523\n"
                "🔹 Build ID: SP1A.210812.016\n🔹 Display ID: A55_V1.0_20250523\n"
                "🔹 Build Date: 23 May 2025\n🔹 Security Patch: 05 May 2023\n"
                "🔹 Dump Type: Full Dump\n🔹 File System: eMMC\n🔹 Userdata FS: F2FS\n"
                "🔹 حجم الملف: 1.7 GB\n🔹 Dump By: UnlockTool\n"
                "━━━━━━━━━━━━\n"
                "تم إعادة رفع الدامب على Google Drive بدلاً من TeraBox لتسهيل التحميل.\n"
                "🔐 كلمة مرور الملف: MobiFirmware.VIP\n"
                "⚠️ تأكد من مطابقة إصدار الهاتف والـ Build قبل التفليش\n"
                "HMAX-UNLOCKER - HithamMax"
            ),
            "en": (
                "🔥 Blackview A55 – Full Dump | UnlockTool 🔥\n"
                "📱 Dump pulled by UnlockTool, previously paid on TeraBox.\n"
                "On members request, re-uploaded to Google Drive - Now FREE:\n"
                "🟢 Paid now FREE 🟢\n"
                "📦 Brand: Blackview | Model: A55 | CPU: MT6761 | Android 11\n"
                "Build: A55_V1.0_20250523 | ID: SP1A.210812.016 | 1.7 GB | Full Dump eMMC F2FS\n"
                "🔐 Password: MobiFirmware.VIP\n⚠️ Check Build before flashing\nHMAX-UNLOCKER"
            ),
            "fr": (
                "🔥 Blackview A55 – Dump Complet | UnlockTool 🔥\n"
                "📱 Dump extrait par UnlockTool, avant sur TeraBox payant.\n"
                "À la demande, re-uploadé sur Google Drive - Maintenant GRATUIT:\n"
                "🟢 Payant maintenant GRATUIT 🟢\n"
                "📦 Brand: Blackview | Model: A55 | CPU: MT6761 | Android 11\n"
                "Build: A55_V1.0_20250523 | ID: SP1A.210812.016 | 1.7 GB | Full Dump eMMC F2FS\n"
                "🔐 Mot de passe: MobiFirmware.VIP\n⚠️ Vérifiez Build avant flash\nHMAX-UNLOCKER"
            ),
        }
        txt = t.get(lang, t["ar"])
        btn_dl = {"ar": "📥 رابط التحميل - 1.7GB FREE", "en": "📥 Download - 1.7GB FREE", "fr": "📥 Lien - 1.7GB GRATUIT"}.get(lang, "📥 Download")
        btn_back = {"ar": "⬅️ رجوع لـ DUMP", "en": "⬅️ Back to DUMP", "fr": "⬅️ Retour à DUMP"}.get(lang, "⬅️ Back")

        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton(btn_dl, url=gdrive_url))
        markup.add(types.InlineKeyboardButton(btn_back, callback_data="dump_main_section"))
        try:
            with open(photo_path, 'rb') as photo:
                bot.send_photo(call.message.chat.id, photo, caption=txt, reply_markup=markup)
        except:
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    elif cd == "dump_model_benco_v60_full":
        markup = types.InlineKeyboardMarkup(row_width=1)
        gdrive_url = "https://drive.google.com/file/d/1IWj92n5541TYoYKXe-sC9eyNkbsrte6f/view"
        photo_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "images",
            "benco_v60_full_dump_cm2.jpg",
        )
        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass
        try:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except Exception:
            pass
        txt = (
            "📱 Benco V60 — FULL DUMP 🔥\n━━━━━━━━━━━━\n"
            "مش كل جهاز هتلاقي له Dump جاهز وقت ما تحتاجه...\nوعشان كده بنستمر في تجهيز ملفات يحتاجها الفني.\n━━━━━━━━━━━━\n"
            "📱 Device: Benco V60\n🔧 Read By: CM2\n📁 File: Full Dump\n"
            "☁️ Hosting: Google Drive\n🔐 Pass: MobiFirmware.VIP\n"
        )
        txt = _dump_card_text(user_id, "dump_model_benco_v60_full", txt)
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📥 Download - Google Drive"), url=gdrive_url))
        markup.add(types.InlineKeyboardButton(_dump_back_label(user_id, "⬅️ Back"), callback_data="dump_benco_section"))
        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(call.message.chat.id, photo, caption=txt, reply_markup=markup)
        except Exception as e:
            print(f"Send BENCO V60 photo failed: {e}")
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    elif cd == "dump_model_hisorl_t901_full":
        markup = types.InlineKeyboardMarkup(row_width=1)
        gdrive_url = "https://drive.google.com/file/d/1IQMjflRd0asfRQl3_z2PaCu6FeAxvzyO/view"
        photo_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "images",
            "hisorl_t901_full_dump_unlocktool.jpg",
        )
        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass
        try:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except Exception:
            pass
        txt = (
            "📱 NEW DUMP | HISORL T901 — FULL DUMP 🔥\n━━━━━━━━━━━━\n"
            "تم سحب الدامب من جهاز فعلي وتجهيزه ورفعه على Google Drive\n"
            "ليستفيد منه أعضاء الجروب وقت الحاجة.\n━━━━━━━━━━━━\n"
            "📱 Device: HISORL T901\n📁 Dump: Full Dump\n🔧 Tool: UnlockTool\n"
            "☁️ Storage: Google Drive\n🔐 Password: MobiFirmware.VIP\n━━━━━━━━━━━━\n"
            "🙏 كل الشكر لأخونا الغالي ĶĦălěď Ķäbô\nعلى مجهوده في سحب الدامب\n"
        )
        txt = _dump_card_text(user_id, "dump_model_hisorl_t901_full", txt)
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📥 Download - Google Drive"), url=gdrive_url))
        markup.add(types.InlineKeyboardButton(_dump_back_label(user_id, "⬅️ Back"), callback_data="dump_hisorl_section"))
        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(call.message.chat.id, photo, caption=txt, reply_markup=markup)
        except Exception as e:
            print(f"Send HISORL T901 photo failed: {e}")
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    # ===== 📱 TAB - YTAB + TAB A9 + Oteeto =====
    elif cd == "dump_tab_section":
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton(
            _dump_btn(user_id, "📱 YTAB - Library"),
            callback_data="dump_ytab_section",
        ))
        markup.add(types.InlineKeyboardButton(
            _dump_btn(user_id, "📱 TAB A9 SM-X110"),
            callback_data="dump_model_tab_a9_sm_x110",
        ))
        markup.add(types.InlineKeyboardButton(
            _dump_btn(user_id, "🔥 The Oteeto TAB 15 - FULL DUMP [CM2] RARE"),
            callback_data="dump_model_the_oteeto_tab_15_full_dump_cm2",
        ))
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "⬅️ Back to DUMP"), callback_data="dump_main_section"))
        section_text = (
            "📱 TAB - Tablets Firmware Library\n"
            "اختر الموديل:\n\n"
            "YTAB + TAB A9 + Oteeto"
        )
        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass
        _hmax_show_menu(call, _dump_localize(user_id, section_text), markup)
        return

    elif cd == "dump_ytab_section":
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton(
            _dump_btn(user_id, "🔥 ULTRA 35 FULL DUMP 3GB [CM2 | Prince Cazanova]"),
            callback_data="dump_model_ytab_ultra_35_full_dump_cm2",
        ))
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "⬅️ Back to TAB"), callback_data="dump_tab_section"))
        section_text = (
            "📱 YTAB - Official Firmware Library\n"
            "━━━━━━━━━━━━\n"
            "🔷 Brand: YTAB\n"
            "📦 Full Dump Library\n"
            "☁️ Google Drive\n"
            "━━━━━━━━━━━━\n"
            "اختر الموديل:"
        )
        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass
        _hmax_show_menu(call, _dump_localize(user_id, section_text), markup)
        return

    elif cd == "dump_model_ytab_ultra_35_full_dump_cm2":
        markup = types.InlineKeyboardMarkup(row_width=1)
        gdrive_url = "https://drive.google.com/file/d/1zplMZgC3PUa_MP0F5BOtosQejZaom4dZ/view"
        photo_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "images",
            "ytab_ultra_35_full_dump_cm2_prince_cazanova.jpg",
        )
        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass
        try:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except Exception:
            pass
        txt = (
            "🔥 YTAB ULTRA 35 — FULL DUMP 🔥\n━━━━━━━━━━━━\n"
            "🌟 BY CM2 ONLY | By Prince Cazanova 🌟\n"
            "📱 Device: YTAB ULTRA 35\n"
            "🔧 Dump Tool: Infinity CM2MT2\n"
            "📦 Dump Size: 3 GB\n"
            "☁️ Uploaded on: Google Drive\n"
            "🔐 Pass: MobiFirmware.VIP\n"
            "━━━━━━━━━━━━\n"
            "Brand: Ytab | Model: ULTRA35\n"
            "Board: k50sv1_64_bsp | Platform: mt6750\n"
            "Android: 10 | Patch: 2025-02-01\n"
            "Build: 07.07.2025 | Display ID: M55P30DDR_BYC_ULTRA35_Ytab_V1.0_20250707\n"
            "CPU: arm64-v8a | Created: CM2MT2 v2.38d1 — 2026-07-08\n"
            "━━━━━━━━━━━━\n"
            "⚠️ تأكد من مطابقة البورد قبل التفليش\n"
            "HMAX hithamMax\n"
        )
        txt = _dump_card_text(user_id, "dump_model_ytab_ultra_35_full_dump_cm2", txt)
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📥 Download - Google Drive 3GB"), url=gdrive_url))
        markup.add(types.InlineKeyboardButton(_dump_back_label(user_id, "⬅️ Back"), callback_data="dump_ytab_section"))
        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(call.message.chat.id, photo, caption=txt, reply_markup=markup)
        except Exception as e:
            print(f"Send YTAB ULTRA 35 photo failed: {e}")
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    elif cd == "dump_model_the_oteeto_tab_15_full_dump_cm2":
        markup = types.InlineKeyboardMarkup(row_width=1)
        gdrive_url = "https://drive.google.com/file/d/19RaJLb3dnlcj3Wj9hdkg8I4aL-tUuHQY/view"
        photo_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "images",
            "the_oteeto_tab_15_full_dump_cm2_rare.jpg",
        )
        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass
        try:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except Exception:
            pass
        txt = (
            "🔥 The Oteeto TAB 15 — FULL DUMP 🔥\n"
            "━━━━━━━━━━━━\n"
            "💎 ملف نادر جدًا، وواحد من الملفات اللي\n"
            "مش هتدور عليه كتير على الإنترنت لأنك ببساطة مش هتلاقيه.\n"
            "━━━━━━━━━━━━\n"
            "📦 إيه اللي وفرناه النهارده؟\n"
            "🔥 Full Dump أصلي تم سحبه مباشرة من الجهاز\n"
            "🔧 تم سحب الملف باستخدام CM2\n"
            "👨‍🔧 ملف مخصص للفنيين وأعمال السوفت وير\n"
            "☁️ تم رفعه وتجهيزه على Google Drive\n"
            "━━━━━━━━━━━━\n"
            "📱 الجهاز:\n"
            "The Oteeto TAB 15\n"
            "📦 نوع الملف:\n"
            "FULL DUMP\n"
            "🔧 Tool:\n"
            "CM2\n"
            "🔐 Password:\n"
            "MobiFirmware.VIP\n"
            "━━━━━━━━━━━━\n"
            "💡 الملفات النادرة اللي غيرك ممكن يدور عليها بالساعات…\n"
            "تلاقيها جاهزة عندنا.\n"
            "━━━━━━━━━━━━\n"
            "HMAX-UNLOCKER HithamMax\n"
        )
        txt = _dump_card_text(user_id, "dump_model_the_oteeto_tab_15_full_dump_cm2", txt)
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📥 Download - Google Drive RARE"), url=gdrive_url))
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "⬅️ Back to TAB"), callback_data="dump_tab_section"))
        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(call.message.chat.id, photo, caption=txt, reply_markup=markup)
        except Exception as e:
            print(f"Send Oteeto TAB 15 photo failed: {e}")
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    elif cd == "dump_wiko_section":
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton(
            _dump_btn(user_id, "🔥 WIKO T10 - FULL DUMP V01.57 [UnlockTool]"),
            callback_data="dump_model_wiko_t10_full_dump_unlocktool",
        ))
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "⬅️ Back to DUMP"), callback_data="dump_main_section"))
        section_text = (
            "📱 WIKO - Firmware Library\n"
            "━━━━━━━━━━━━\n"
            "🔷 Brand: WIKO\n"
            "📦 Full Dump Library\n"
            "☁️ Google Drive\n"
            "━━━━━━━━━━━━\n"
            "اختر الموديل:"
        )
        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass
        _hmax_show_menu(call, _dump_localize(user_id, section_text), markup)
        return

    elif cd == "dump_model_wiko_t10_full_dump_unlocktool":
        markup = types.InlineKeyboardMarkup(row_width=1)
        gdrive_url = "https://drive.google.com/file/d/1HGMTtBPH4TNYXIusU4G1ZO3scGphM7cq/view"
        photo_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "images",
            "wiko_t10_full_dump_v01_57_unlocktool_hamallah.jpg",
        )
        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass
        try:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except Exception:
            pass
        txt = (
            "🔥 جديد الدامبات | WIKO T10 — FULL DUMP 🔥\n"
            "━━━━━━━━━━━━\n"
            "📱 اسم الجهاز: WIKO T10\n"
            "📱 رقم الموديل: W-V673-01 / W-V673-02\n"
            "🔧 Firmware: W-V673-V01.57-11.0-GBL\n"
            "🔧 Full Dump — مسحوب بالـ Unlock Tool\n"
            "✍️ By Hamallah\n"
            "━━━━━━━━━━━━\n"
            "📋 مواصفات الجهاز\n"
            "🖥️ الشاشة: 6.5 بوصة IPS LCD\n"
            "📐 الدقة: 720 × 1600\n"
            "🧠 المعالج: MediaTek Helio A22 — MT6761\n"
            "CPU: رباعي النواة 2.0GHz Cortex-A53\n"
            "GPU: PowerVR GE8300\n"
            "💾 الرام: 2GB\n"
            "💾 التخزين: 64GB + دعم microSD حتى 512GB\n"
            "📷 الكاميرا الخلفية: 13MP مع AF\n"
            "📷 الكاميرا الأمامية: 5MP\n"
            "🔋 البطارية: 5000mAh\n"
            "🤖 النظام: Android 11 Go Edition\n"
            "📏 الأبعاد: 163.94 × 75.79 × 8.97 مم\n"
            "⚖️ الوزن: حوالي 192 جرام\n"
            "📡 الشبكات: 2G / 3G / 4G LTE\n"
            "🔗 Bluetooth 5.0 + Wi-Fi + GPS + FM\n"
            "━━━━━━━━━━━━\n"
            "👤 الدامب من سحب أخونا عضو الجروب\n"
            "🙏 حماه الله عبدالمالك\n"
            "كل الشكر والتقدير ليه على المشاركة\n"
            "━━━━━━━━━━━━\n"
            "☁️ تم رفع الدامب على Google Drive\n"
            "🔐 Pass File: MobiFirmware.VIP\n"
            "━━━━━━━━━━━━\n"
            "HMAX-UNLOCKER HithamMax\n"
        )
        txt = _dump_card_text(user_id, "dump_model_wiko_t10_full_dump_unlocktool", txt)
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📥 Download - Google Drive"), url=gdrive_url))
        markup.add(types.InlineKeyboardButton(_dump_back_label(user_id, "⬅️ Back"), callback_data="dump_wiko_section"))
        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(call.message.chat.id, photo, caption=txt, reply_markup=markup)
        except Exception as e:
            print(f"Send WIKO T10 photo failed: {e}")
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    elif cd == "dump_villaon_section":
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton(
            _dump_btn(user_id, "🔥 VILLAON V20 - FULL DUMP V01.57 [UnlockTool]"),
            callback_data="dump_model_villaon_v20_full_dump_unlocktool",
        ))
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "⬅️ Back to DUMP"), callback_data="dump_main_section"))
        section_text = (
            "📱 VILLAON - Firmware Library\n"
            "━━━━━━━━━━━━\n"
            "🔷 Brand: VILLAON\n"
            "📦 Full Dump Library\n"
            "☁️ Google Drive\n"
            "━━━━━━━━━━━━\n"
            "اختر الموديل:"
        )
        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass
        _hmax_show_menu(call, _dump_localize(user_id, section_text), markup)
        return

    elif cd == "dump_model_villaon_v20_full_dump_unlocktool":
        markup = types.InlineKeyboardMarkup(row_width=1)
        gdrive_url = "https://drive.google.com/file/d/10EaY1ggOVvB2Yrgf7BZYSqMcu23fIB7I/view"
        photo_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "images",
            "villaon_v20_full_dump_v01_57_unlocktool_hamallah.jpg",
        )
        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass
        try:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except Exception:
            pass
        txt = (
            "🔥 VILLAON V20 — FULL DUMP 🔥\n"
            "━━━━━━━━━━━━\n"
            "📱 اسم الجهاز: VILLAON V20\n"
            "📦 نوع الملف: Full Dump Firmware\n"
            "🔧 Firmware: W-V673-V01.57-11.0-GBL\n"
            "🔧 Full Dump — مسحوب بالـ Unlock Tool\n"
            "✍️ By Hamallah\n"
            "━━━━━━━━━━━━\n"
            "👤 الدامب من سحب عضو الجروب أخونا\n"
            "🙏 حماه الله عبدالمالك\n"
            "كل الشكر والتقدير ليه على المشاركة ❤️\n"
            "━━━━━━━━━━━━\n"
            "☁️ تم رفع الدامب على Google Drive\n"
            "📥 للتحميل\n"
            "🔐 Pass File: MobiFirmware.VIP\n"
            "━━━━━━━━━━━━\n"
            "🔧 Full Dump | مسحوب بالـ Unlock Tool\n"
            "HMAX-UNLOCKER HithamMax\n"
        )
        txt = _dump_card_text(user_id, "dump_model_villaon_v20_full_dump_unlocktool", txt)
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📥 Download - Google Drive"), url=gdrive_url))
        markup.add(types.InlineKeyboardButton(_dump_back_label(user_id, "⬅️ Back"), callback_data="dump_villaon_section"))
        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(call.message.chat.id, photo, caption=txt, reply_markup=markup)
        except Exception as e:
            print(f"Send VILLAON V20 photo failed: {e}")
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    elif cd == "dump_hmd_section":
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton(
            _dump_btn(user_id, "🔥 HMD AURA TA-1631 2 ROMs Official [Unbrick]"),
            callback_data="dump_model_hmd_aura_ta1631",
        ))
        markup.add(types.InlineKeyboardButton(
            _dump_btn(user_id, "⬅️ Back to DUMP"),
            callback_data="dump_main_section",
        ))
        section_text = (
            "📱 HMD - Official Firmware Library\n"
            "━━━━━━━━━━━━\n"
            "🔷 Brand: HMD\n"
            "📦 Official Stock ROMs\n"
            "☁️ Google Drive - Direct Link\n"
            "━━━━━━━━━━━━\n"
            "اختر الموديل:"
        )
        try:
            bot.answer_callback_query(call.id)
        except Exception as e:
            print(f"Answer HMD section callback failed: {e}")
        _hmax_show_menu(call, _dump_localize(user_id, section_text), markup)
        return

    elif cd == "dump_model_hmd_aura_ta1631":
        markup = types.InlineKeyboardMarkup(row_width=1)
        gdrive_url = "https://drive.google.com/file/d/1hp-B3jh0q0tTGNYLxq8R4yWy4Y0W_3tw/view"
        photo_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "images",
            "hmd_aura_ta1631_hmax_final.jpg",
        )
        try:
            bot.answer_callback_query(call.id)
        except Exception as e:
            print(f"Answer HMD AURA callback failed: {e}")
        try:
            bot.delete_message(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
            )
        except Exception as e:
            print(f"Delete HMD AURA menu failed: {e}")

        text = (
            "📱 HMD AURA - TA-1631 - فلاشات رسمية 📱\n"
            "━━━━━━━━━━━━\n"
            "📱 Device: HMD AURA\n"
            "🏷️ Model: TA-1631\n"
            "🔧 Codename: ROCKY - Unisoc SC9863A1 - Android 13\n"
            "📦 File: 2 Official Stock ROMs\n"
            "🏗️ Build 1: rck_116A-0-00WW-B01\n"
            "🏗️ Build 2: rck_1100-0-00WW-B01\n"
            "✅ 100% رسمية أصلية معتمدة\n"
            "━━━━━━━━━━━━\n"
            "🛠️ تحل مشاكل السوفتوير مثل:\n"
            "💀 موت الهاتف أثناء التفليش الخاطئ\n"
            "⚠️ مشاكل في نظام السوفتوير\n"
            "🔧 حل مشاكل الإقلاع والتعليق والتهنيج\n"
            "━━━━━━━━━━━━\n"
            "📱 مواصفات: 6.52 HD+ IPS - SC9863A1 - 2/3GB - 32GB - 5000mAh\n"
            "☁️ Upload: Google Drive - رابط مباشر مجانا\n"
            "🔐 Pass: MobiFirmware.VIP"
        )
        text = _dump_card_text(user_id, "dump_model_hmd_aura_ta1631", text)
        markup.add(types.InlineKeyboardButton(
            _dump_btn(user_id, "📥 التحميل مجانا - Google Drive"),
            url=gdrive_url,
        ))
        markup.add(types.InlineKeyboardButton(
            _dump_back_label(user_id, "⬅️ Back"),
            callback_data="dump_hmd_section",
        ))
        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(
                    call.message.chat.id,
                    photo,
                    caption=text,
                    reply_markup=markup,
                )
        except Exception as e:
            print(f"Send HMD AURA photo failed: {e}")
            bot.send_message(
                call.message.chat.id,
                text,
                reply_markup=markup,
            )
        return

    elif cd == "dump_itel_full_section":
        markup = types.InlineKeyboardMarkup(row_width=1)
        lang = hmaxi18n.get_language(user_id)
        translations = {
            "ar": {
                "title": "📱 ITEL DUMP",
                "p37": "🔥 P37 - P651W - Full Dump + Nv",
                "a49": "🔥 A661L - A49 (A58 Pro) [PANDORA] - نادر NEW",
                "back": "🔙 رجوع",
            },
            "en": {
                "title": "📱 ITEL DUMP",
                "p37": "🔥 P37 - P651W - Full Dump + Nv",
                "a49": "🔥 A661L - A49 (A58 Pro) [PANDORA] - Rare NEW",
                "back": "🔙 Back",
            },
            "fr": {
                "title": "📱 DUMP ITEL",
                "p37": "🔥 P37 - P651W - Full Dump + Nv",
                "a49": "🔥 A661L - A49 (A58 Pro) [PANDORA] - Rare NEW",
                "back": "🔙 Retour",
            },
        }
        labels = translations.get(lang, translations["ar"])
        txt = labels["title"]
        markup.add(types.InlineKeyboardButton(
            labels["p37"],
            callback_data="dump_model_itel_p37_p651w",
        ))
        markup.add(types.InlineKeyboardButton(
            labels["a49"],
            callback_data="dump_model_itel_a49_a661l",
        ))
        markup.add(types.InlineKeyboardButton(
            _dump_btn(user_id, "🔥 Itel L6503 Vision 2 - 3 Tools Dumps"),
            callback_data="dump_model_itel_l6503_vision2",
        ))
        if lang == "en":
            l6503_3tools_label = "🔥 Itel L6503 Vision 2 - 3 Tools 3 Dumps"
        elif lang == "fr":
            l6503_3tools_label = "🔥 Itel L6503 Vision 2 - 3 Outils 3 Dumps"
        else:
            l6503_3tools_label = "🔥 Itel L6503 Vision 2 - 3 TOOLS 3 DUMPS"
        markup.add(types.InlineKeyboardButton(
            l6503_3tools_label,
            callback_data="dump_model_itel_l6503_vision_2_3dumps",
        ))
        markup.add(types.InlineKeyboardButton(
            _dump_btn(user_id, "🔥 iTEL A06 A669W - FULL DUMP 2GB V1604 [UnlockTool]"),
            callback_data="dump_model_itel_a06_a669w_full_dump_unlocktool",
        ))
        markup.add(types.InlineKeyboardButton(
            _dump_btn(user_id, "🔥 ITEL S23 - S665LN - F065 - 2 Parts [PANDORA]"),
            callback_data="dump_model_itel_s23_s665ln",
        ))
        # ITEL lives inside the DUMP brand menu, so back returns there.
        markup.add(types.InlineKeyboardButton(labels["back"], callback_data="dump_main_section"))
        try:
            bot.answer_callback_query(call.id)
        except Exception as e:
            print(f"Answer ITEL dump callback failed: {e}")
        _hmax_show_menu(call, txt, markup)
        return

    elif cd == "dump_model_itel_a49_a661l":
        lang = hmaxi18n.get_language(user_id)
        terabox_url = "https://www.terabox.app/arabic/sharing/link?surl=aylVN-8Y7P9jI6ye9JpsMQ"
        photo_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "images",
            "itel_a49_a661l_a58pro_pandora_hmax.jpg",
        )
        translations = {
            "ar": {
                "download": "📥 تحميل Terabox",
                "back": "⬅️ رجوع لـ ITEL",
            },
            "en": {
                "download": "📥 Download Terabox",
                "back": "⬅️ Back to ITEL",
            },
            "fr": {
                "download": "📥 Télécharger Terabox",
                "back": "⬅️ Retour à ITEL",
            },
        }
        labels = translations.get(lang, translations["ar"])
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton(labels["download"], url=terabox_url))
        markup.add(types.InlineKeyboardButton(
            labels["back"],
            callback_data="dump_itel_full_section",
        ))

        try:
            bot.answer_callback_query(call.id)
        except Exception as e:
            print(f"Answer ITEL A49 callback failed: {e}")
        try:
            bot.delete_message(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
            )
        except Exception as e:
            print(f"Delete ITEL A49 menu failed: {e}")

        txt = (
            "🔥 Itel A661L - Itel A49 (A58 Pro) 🔥\n"
            "📱 الموديل: A661L / A49 / A58 Pro\n"
            "🛠️ Dump BY Pandora Tool\n"
            "🔑 Pass: MobiFirmware.VIP\n"
            "💎 دامب جهاز Itel A49 جهاز مش موجود بالوجود\n"
            "✅ مجرب 100% من جهاز سليم\n"
            "⚠️ احتفظ بملفات الشبكة قبل التفليش\n"
            "رزق الله الجميع\n"
            "HMAX-UNLOCKER"
        )
        txt = _dump_card_text(user_id, "dump_model_itel_a49_a661l", txt)
        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(
                    call.message.chat.id,
                    photo,
                    caption=txt,
                    reply_markup=markup,
                )
        except Exception as e:
            print(f"Send ITEL A49 photo failed: {e}")
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    elif cd == "dump_model_itel_a06_a669w_full_dump_unlocktool":
        markup = types.InlineKeyboardMarkup(row_width=1)
        gdrive_url = "https://drive.google.com/file/d/1KJX3Zv3JPcke4sWTE8ubE-3xPAevhNjO/view"
        photo_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "images",
            "itel_a06_a669w_full_dump_v1604_unlocktool_hamallah.jpg",
        )
        try:
            bot.answer_callback_query(call.id)
        except Exception as e:
            print(f"Answer ITEL A06 callback failed: {e}")
        try:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except Exception as e:
            print(f"Delete ITEL A06 menu failed: {e}")

        txt = (
            "🔥 iTEL A06 - A669W — FULL DUMP 🔥\n"
            "━━━━━━━━━━━━\n"
            "📱 اسم الجهاز: iTEL A669W\n"
            "📱 رقم الموديل: A669W\n"
            "🔧 Firmware: A669W-SA375A-UGO-OP-250114V1604\n"
            "🔧 Full Dump — مسحوب بالـ UnlockTool\n"
            "✍️ By Hamallah\n"
            "━━━━━━━━━━━━\n"
            "📋 معلومات الدامب\n"
            "📦 نوع الملف: Full Dump\n"
            "📦 حجم الملف: حوالي 2.00 GB\n"
            "📦 صيغة الملف: ZIP\n"
            "🔧 أداة السحب: UnlockTool\n"
            "🔧 Build: 250114\n"
            "🔧 Version: V1604\n"
            "━━━━━━━━━━━━\n"
            "👤 الدامب من سحب أخونا عضو الجروب\n"
            "🙏 حماه الله عبدالمالك\n"
            "كل الشكر والتقدير ليه على المشاركة والمساهمة في إفادة الفنيين\n"
            "━━━━━━━━━━━━\n"
            "☁️ تم رفع الدامب على Google Drive\n"
            "🔐 Pass File: MobiFirmware.VIP\n"
            "━━━━━━━━━━━━\n"
            "🔧 Full Dump | UnlockTool | جاهز لأعمال السوفت وير والصيانة\n"
            "HMAX hithamMax\n"
        )
        txt = _dump_card_text(user_id, "dump_model_itel_a06_a669w_full_dump_unlocktool", txt)
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📥 Download - Google Drive 2GB"), url=gdrive_url))
        markup.add(types.InlineKeyboardButton(_dump_back_label(user_id, "⬅️ Back"), callback_data="dump_itel_full_section"))
        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(
                    call.message.chat.id,
                    photo,
                    caption=txt,
                    reply_markup=markup,
                )
        except Exception as e:
            print(f"Send ITEL A06 photo failed: {e}")
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    elif cd == "dump_model_itel_s23_s665ln":
        markup = types.InlineKeyboardMarkup(row_width=1)
        lang = hmaxi18n.get_language(user_id)
        terabox_url = "https://www.terabox.app/arabic/sharing/link?surl=RMigbSPD9-7YafQPj0LlMQ"
        photo_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "images",
            "itel_s23_s665ln_f065_pandora_hmax.jpg",
        )
        try:
            bot.answer_callback_query(call.id)
        except Exception as e:
            print(f"Answer ITEL S23 callback failed: {e}")
        try:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except Exception as e:
            print(f"Delete ITEL S23 menu failed: {e}")

        txts = {
            "ar": (
                "🔥 ITEL S23 - S665LN-F065-S-GL-V305-20240715 🔥\\n"
                "📱 Model: S23 - S665LN\\n"
                "🔖 Version: F065-S-GL-V305-20240715\\n"
                "🛠️ Dump By Pandora Tool\\n"
                "📦 File uploaded in 2 parts\\n"
                "☁️ Terabox\\n"
                "🔑 Pass: MobiFirmware.VIP\\n"
                "⚠️ ملاحظه افتح VPN سايفون على شان يظهر لك رابط التحميل\\n"
                "HMAX-UNLOCKER"
            ),
            "en": (
                "🔥 ITEL S23 - S665LN 🔥\\n"
                "Model: S23 S665LN\\n"
                "Version: F065-S-GL-V305-20240715\\n"
                "Dump By Pandora\\n"
                "2 Parts\\n"
                "Terabox\\n"
                "Pass: MobiFirmware.VIP\\n"
                "Note: Open Psiphon VPN\\n"
                "HMAX"
            ),
            "fr": (
                "🔥 ITEL S23 - S665LN 🔥\\n"
                "Modèle: S23 S665LN\\n"
                "Version: F065-S-GL-V305-20240715\\n"
                "Dump par Pandora\\n"
                "2 Parties\\n"
                "Terabox\\n"
                "Pass: MobiFirmware.VIP\\n"
                "Note: Ouvrez VPN Psiphon\\n"
                "HMAX"
            ),
        }
        txt = txts.get(lang, txts["ar"])
        btn_labels = {
            "ar": "📥 تحميل Terabox - جزئين - VPN مطلوب",
            "en": "📥 Download Terabox - 2 parts - VPN required",
            "fr": "📥 Télécharger Terabox - 2 parties - VPN requis",
        }
        markup.add(types.InlineKeyboardButton(btn_labels.get(lang, btn_labels["ar"]), url=terabox_url))
        markup.add(types.InlineKeyboardButton(_dump_back_label(user_id, "⬅️ Back"), callback_data="dump_itel_full_section"))
        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(call.message.chat.id, photo, caption=txt, reply_markup=markup)
        except Exception as e:
            print(f"Send ITEL S23 photo failed: {e}")
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    elif cd == "dump_model_itel_p37_p651w":
        markup = types.InlineKeyboardMarkup(row_width=1)
        gdrive_url = "https://drive.google.com/file/d/1-FOKgpMC-oVjuyVdIS2LNeMqcQvP704J/view"
        photo_path = "images/itel_p37_p651w.jpg"

        try:
            bot.answer_callback_query(call.id)
        except Exception as e:
            print(f"Answer ITEL model callback failed: {e}")
        try:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except Exception as e:
            print(f"Delete ITEL model menu failed: {e}")

        txt = (
            "🔥 ITEL P37 - P651W 🔥\n"
            "━━━━━━━━━━━━\n"
            "📱 Brand: ITEL\n"
            "📌 Model: P37\n"
            "🔧 Code: P651W\n"
            "🏗️ Build: F3116-10.0-OP-V70-2023022\n"
            "💾 Type: Unlock Tool Full Dump + Nv File\n"
            "━━━━━━━━━━━━\n"
            "🔐 Pass: MobiFirmware.VIP"
        )
        txt = _dump_card_text(user_id, "dump_model_itel_p37_p651w", txt)
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📥 Download"), url=gdrive_url))
        markup.add(types.InlineKeyboardButton(_dump_back_label(user_id, "⬅️ Back"), callback_data="dump_itel_full_section"))
        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(
                    call.message.chat.id,
                    photo,
                    caption=txt,
                    reply_markup=markup,
                )
        except Exception as e:
            print(f"Send ITEL P37 photo failed: {e}")
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    elif cd == "dump_model_itel_l6503_vision2":
        markup = types.InlineKeyboardMarkup(row_width=1)
        photo_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "images",
            "itel_l6503_vision2_3dumps.jpg",
        )
        try:
            bot.answer_callback_query(call.id)
        except Exception as e:
            print(f"Answer ITEL Vision 2 callback failed: {e}")
        try:
            bot.delete_message(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
            )
        except Exception as e:
            print(f"Delete ITEL Vision 2 menu failed: {e}")

        txt = (
            "📱 Itel L6503 - Itel Vision 2 - 3 Dumps 📱\n"
            "━━━━━━━━━━━━\n"
            "🏷️ Model: L6503\n"
            "🔧 Chipset: Unisoc SC9863A Octa 1.6GHz IMG8322\n"
            "📦 RAM: 2GB/3GB - Storage: 32GB/64GB eMMC\n"
            "📱 Display: 6.6 HD+ 720x1600\n"
            "🔋 Battery: 5000mAh - Android 10 Go\n"
            "━━━━━━━━━━━━\n"
            "📦 Dump 1 - CM2:\n"
            "🔖 Build: L6503-F6315-10.0-OP-V049-20221213\n"
            "📦 Size: 3GB\n"
            "📦 Dump 2 - UnlockTool Full Dump:\n"
            "🔖 Build: L6503-F6315-10.0-OP-V049-20221213\n"
            "📦 Size: 1.7GB\n"
            "📦 Dump 3 - Pandora Tool:\n"
            "📦 Size: 1.7GB\n"
            "━━━━━━━━━━━━\n"
            "☁️ Upload: Google Drive - 3 Links\n"
            "🔐 Pass: MobiFirmware.VIP\n"
            "🎯 هدفنا الفني يلاقي اللي محتاجه من غير ما يلف كتير\n"
        )
        txt = _dump_card_text(user_id, "dump_model_itel_l6503_vision2", txt)
        markup.add(types.InlineKeyboardButton(
            _dump_btn(user_id, "📥 CM2 - 3GB - Drive"),
            url="https://drive.google.com/file/d/1cUD2DdoJUYqCZcQA4mMD0PqjKv2QLDwY/view",
        ))
        markup.add(types.InlineKeyboardButton(
            _dump_btn(user_id, "📥 UnlockTool - 1.7GB - Drive"),
            url="https://drive.google.com/file/d/1Falf33XhyUvzkjCDb5-UQepVprz1aXp2/view",
        ))
        markup.add(types.InlineKeyboardButton(
            _dump_btn(user_id, "📥 Pandora - 1.7GB - Drive"),
            url="https://drive.google.com/file/d/1qE-Cla3_cd0_bL-P25fO11izH03Q4SuO/view",
        ))
        markup.add(types.InlineKeyboardButton(
            _dump_back_label(user_id, "⬅️ Back"),
            callback_data="dump_itel_full_section",
        ))
        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(
                    call.message.chat.id,
                    photo,
                    caption=txt,
                    reply_markup=markup,
                )
        except Exception as e:
            print(f"Send ITEL Vision 2 photo failed: {e}")
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    elif cd == "dump_model_itel_l6503_vision_2_3dumps":
        markup = types.InlineKeyboardMarkup(row_width=1)
        lang = hmaxi18n.get_language(user_id)
        # روابط الـ 3 دامبات
        gdrive_cm2 = "https://drive.google.com/file/d/1cUD2DdoJUYqCZcQA4mMD0PqjKv2QLDwY/view"
        gdrive_unlock = "https://drive.google.com/file/d/1Falf33XhyUvzkjCDb5-UQepVprz1aXp2/view"
        gdrive_pandora = "https://drive.google.com/file/d/1qE-Cla3_cd0_bL-P25fO11izH03Q4SuO/view"
        photo_path = "images/itel_l6503_vision_2_3tools_3dumps.jpg"
        try:
            bot.answer_callback_query(call.id)
        except Exception as e:
            print(f"Answer ITEL Vision 2 3-tools callback failed: {e}")
        try:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except Exception as e:
            print(f"Delete ITEL Vision 2 3-tools menu failed: {e}")

        if lang == "en":
            txt = (
                "📱 Itel L6503 — Itel Vision 2 — 3 TOOLS 3 DUMPS 🔥\n"
                "Today, with a bit of spare time, we decided to give budget devices some attention, because a budget device deserves more than one dump 💛\n"
                "Our goal is always for the technician to find what they need without going around in circles 🔥\n"
                "━━━━━━━━━━━━━━━━━━\n"
                "🛠️ Dump extracted with 3 different tools:\n"
                "🔹 CM2\n"
                "L6503-F6315-10.0-OP-V049-20221213\n"
                "📦 Size: 3 GB\n"
                "🔹 UnlockTool\n"
                "L6503-F6315-10.0-OP-V049-20221213 Full Dump\n"
                "📦 Size: 1.7 GB\n"
                "🔹 Pandora Tool\n"
                "Itel_L6503_DUMP_0610537119003411_(2026-9-8_8-46-19) Full Dump\n"
                "📦 Size: 1.7 GB\n"
                "Uploaded to Google Drive\n"
                "🔐 Pass File: MobiFirmware.VIP\n"
                "━━━━━━━━━━━━━━━━━━\n"
                "📋 Device Specs\n"
                "• Chipset: Unisoc SC9863A\n"
                "• CPU: Octa-Core 1.6 GHz\n"
                "• GPU: IMG8322\n"
                "• RAM: 2GB / 3GB\n"
                "• Storage: 32GB / 64GB eMMC\n"
                "• Display: 6.6\" HD+ — 720×1600\n"
                "• Rear Camera: 13MP + 0.08MP\n"
                "• Front Camera: 5MP\n"
                "• Battery: 5000mAh\n"
                "• OS: Android 10 Go Edition\n"
                "━━━━━━━━━━━━━━━━━━\n"
                "💎 3 TOOLS — 3 DUMPS — MORE OPTIONS FOR TECHNICIANS\n"
                "HMAX hithamMax - PROFESSIONAL FIRMWARE SOLUTIONS\n"
            )
            btn_cm2 = "📥 CM2 - 3GB - L6503-F6315-10.0-OP-V049"
            btn_unlock = "📥 UnlockTool - 1.7GB Full Dump"
            btn_pandora = "📥 Pandora - 1.7GB Full Dump"
            btn_back = "⬅️ Back"
        elif lang == "fr":
            txt = (
                "📱 Itel L6503 — Itel Vision 2 — 3 OUTILS 3 DUMPS 🔥\n"
                "Aujourd'hui, nous nous intéressons aux appareils d'entrée de gamme, car un appareil économique mérite plus d'un dump 💛\n"
                "Objectif : que le technicien trouve vite ce qu'il lui faut 🔥\n"
                "━━━━━━━━━━━━━━━━━━\n"
                "🛠️ Dump extrait avec 3 outils :\n"
                "🔹 CM2\n"
                "L6503-F6315-10.0-OP-V049-20221213\n"
                "📦 Taille : 3 GB\n"
                "🔹 UnlockTool\n"
                "L6503-F6315-10.0-OP-V049-20221213 Full Dump\n"
                "📦 Taille : 1.7 GB\n"
                "🔹 Pandora Tool\n"
                "Itel_L6503_DUMP_0610537119003411_(2026-9-8_8-46-19) Full Dump\n"
                "📦 Taille : 1.7 GB\n"
                "Envoyé sur Google Drive\n"
                "🔐 Mot de passe : MobiFirmware.VIP\n"
                "━━━━━━━━━━━━━━━━━━\n"
                "📋 Fiche technique\n"
                "• Chipset : Unisoc SC9863A\n"
                "• CPU : Octa-Core 1.6 GHz\n"
                "• GPU : IMG8322\n"
                "• RAM : 2 Go / 3 Go\n"
                "• Stockage : 32 Go / 64 Go eMMC\n"
                "• Écran : 6.6\" HD+ — 720×1600\n"
                "• Caméra arrière : 13 MP + 0.08 MP\n"
                "• Caméra frontale : 5 MP\n"
                "• Batterie : 5000 mAh\n"
                "• OS : Android 10 Go Edition\n"
                "━━━━━━━━━━━━━━━━━━\n"
                "💎 3 OUTILS — 3 DUMPS — POUR LES TECHNICIENS\n"
                "HMAX hithamMax - SOLUTIONS FIRMWARE PROFESSIONNELLES\n"
            )
            btn_cm2 = "📥 CM2 - 3GB - L6503-F6315-10.0-OP-V049"
            btn_unlock = "📥 UnlockTool - 1.7GB Full Dump"
            btn_pandora = "📥 Pandora - 1.7GB Full Dump"
            btn_back = "⬅️ Retour"
        else:  # ar هو الافتراضي
            txt = (
                "📱 Itel L6503 — Itel Vision 2 — 3 TOOLS 3 DUMPS 🔥\n"
                "النهارده ومع شوية وقت فاضي قلنا ندي شوية اهتمام لأجهزة الفئة الاقتصادية، لأن الجهاز الاقتصادي يستاهل يكون ليه أكتر من دامب 💛\n"
                "ولأن هدفنا دايمًا إن الفني يلاقي اللي محتاجه من غير ما يلف حوالين نفسه كتير 🔥\n"
                "━━━━━━━━━━━━━━━━━━\n"
                "🛠️ تم سحب الدامب بواسطة 3 Tools مختلفة:\n"
                "🔹 CM2\n"
                "L6503-F6315-10.0-OP-V049-20221213\n"
                "📦 الحجم: 3 GB\n"
                "🔹 UnlockTool\n"
                "L6503-F6315-10.0-OP-V049-20221213 Full Dump\n"
                "📦 الحجم: 1.7 GB\n"
                "🔹 Pandora Tool\n"
                "Itel_L6503_DUMP_0610537119003411_(2026-9-8_8-46-19) Full Dump\n"
                "📦 الحجم: 1.7 GB\n"
                "تم الرفع على Google Drive\n"
                "🔐 Pass File: MobiFirmware.VIP\n"
                "━━━━━━━━━━━━━━━━━━\n"
                "📋 Device Specs\n"
                "• Chipset: Unisoc SC9863A\n"
                "• CPU: Octa-Core 1.6 GHz\n"
                "• GPU: IMG8322\n"
                "• RAM: 2GB / 3GB\n"
                "• Storage: 32GB / 64GB eMMC\n"
                "• Display: 6.6\" HD+ — 720×1600\n"
                "• Rear Camera: 13MP + 0.08MP\n"
                "• Front Camera: 5MP\n"
                "• Battery: 5000mAh\n"
                "• OS: Android 10 Go Edition\n"
                "━━━━━━━━━━━━━━━━━━\n"
                "💎 3 TOOLS — 3 DUMPS — MORE OPTIONS FOR TECHNICIANS\n"
                "HMAX hithamMax - PROFESSIONAL FIRMWARE SOLUTIONS\n"
            )
            btn_cm2 = "📥 CM2 - 3GB - L6503-F6315-10.0-OP-V049"
            btn_unlock = "📥 UnlockTool - 1.7GB Full Dump"
            btn_pandora = "📥 Pandora - 1.7GB Full Dump"
            btn_back = "⬅️ رجوع"
        markup.add(types.InlineKeyboardButton(btn_cm2, url=gdrive_cm2))
        markup.add(types.InlineKeyboardButton(btn_unlock, url=gdrive_unlock))
        markup.add(types.InlineKeyboardButton(btn_pandora, url=gdrive_pandora))
        markup.add(types.InlineKeyboardButton(btn_back, callback_data="dump_itel_full_section"))
        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(call.message.chat.id, photo, caption=txt, reply_markup=markup)
        except Exception as e:
            print(f"Send ITEL Vision 2 3-tools photo failed: {e}")
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    elif cd == "dump_motorola_section":
        lang = hmaxi18n.get_language(user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        if lang == "en":
            section_txt = "📱 Motorola Section\nChoose the model:"
            btn_back = "⬅️ Back"
        elif lang == "fr":
            section_txt = "📱 Section Motorola\nChoisissez le modèle :"
            btn_back = "⬅️ Retour"
        else:  # ar هو الافتراضي
            section_txt = "📱 قسم Motorola\nاختر الموديل:"
            btn_back = "⬅️ رجوع"
        markup.add(types.InlineKeyboardButton(
            _dump_btn(user_id, "📱 Motorola XT2523-7 - Moto E15 5G FULL DUMP [AMT TOOL 2.9GB]"),
            callback_data="dump_model_motorola_xt2523_7_moto_e15",
        ))
        markup.add(types.InlineKeyboardButton(
            _dump_btn(user_id, "🔥 Moto E13 XT2345-4 - FULL DUMP"),
            callback_data="dump_model_moto_e13_xt2345_4_pandora_full_dump",
        ))
        markup.add(types.InlineKeyboardButton(btn_back, callback_data="dump_main_section"))
        try:
            bot.answer_callback_query(call.id)
        except Exception as e:
            print(f"Answer Motorola section callback failed: {e}")
        _hmax_show_menu(call, section_txt, markup)
        return

    elif cd == "dump_model_moto_e13_xt2345_4_pandora_full_dump":
        markup = types.InlineKeyboardMarkup(row_width=1)
        gdrive_url = "https://drive.google.com/file/d/101c8ovGsl5Mfg1UrkPRZv9L9OYZUKBg6/view"
        photo_path = "images/motorola_moto_e13_xt2345-4_pandora_hmax_teal.jpg"
        try:
            bot.answer_callback_query(call.id)
        except Exception as e:
            print(f"Answer Motorola E13 callback failed: {e}")
        try:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except Exception as e:
            print(f"Delete Motorola E13 menu failed: {e}")
        txt = (
            "🔥 Moto E13 — XT2345-4 — FULL DUMP 🔥\n"
            "━━━━━━━━━━━━\n"
            "🔨 DUMP BY PND TOOL\n"
            "تم توفير Full Dump مجرب وموثوق للفنيين.\n"
            "━━━━━━━━━━━━\n"
            "📦 بيانات الدامب:\n"
            "• Model: Moto E13\n"
            "• Model Number: XT2345-4\n"
            "• Tool: PND Tool\n"
            "• Status: مجرب وموثوق ✅\n"
            "• الرفع: Google Drive\n"
            "━━━━━━━━━━━━\n"
            "🔐 Password: MobiFirmware.VIP\n"
        )
        txt = _dump_card_text(user_id, "dump_model_moto_e13_xt2345_4_pandora_full_dump", txt)
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📥 Download"), url=gdrive_url))
        markup.add(types.InlineKeyboardButton(_dump_back_label(user_id, "⬅️ Back"), callback_data="dump_motorola_section"))
        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(call.message.chat.id, photo, caption=txt, reply_markup=markup)
        except Exception as e:
            print(f"Send Motorola E13 photo failed: {e}")
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    elif cd == "dump_model_motorola_xt2523_7_moto_e15":
        lang = hmaxi18n.get_language(user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        gdrive_url = "https://drive.google.com/file/d/16E-6KmWMco6QT-t-H3Mhk5xCCS6j8urw/view"
        photo_path = "images/motorola_xt2523_7_moto_e15_5g_full_dump_amt.jpg"
        try:
            bot.answer_callback_query(call.id)
        except Exception as e:
            print(f"Answer Motorola E15 callback failed: {e}")
        try:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except Exception as e:
            print(f"Delete Motorola E15 menu failed: {e}")

        if lang == "en":
            txt = (
                "🌟 Today we're bringing you a new, important dump 🌟\n"
                "━━━━━━━━━━━━\n"
                "📱 Motorola XT2523-7\n"
                "🔥 Moto E15 5G\n"
                "💾 FULL DUMP\n"
                "🔧 Pulled By: AMT TOOL\n"
                "📦 Dump Size: 2.9 GB\n"
                "☁️ Uploaded To: Google Drive\n"
                "🔐 Pass File: MobiFirmware.VIP\n"
                "━━━━━━━━━━━━\n"
                "✨ Full dump ready for technicians\n"
                "HMAX hithamMax\n"
            )
            btn_download = "📥 Download - Google Drive 2.9GB"
            btn_back = "⬅️ Back"
        elif lang == "fr":
            txt = (
                "🌟 Aujourd'hui, nous vous proposons un nouveau dump important 🌟\n"
                "━━━━━━━━━━━━\n"
                "📱 Motorola XT2523-7\n"
                "🔥 Moto E15 5G\n"
                "💾 FULL DUMP\n"
                "🔧 Extrait par : AMT TOOL\n"
                "📦 Taille du dump : 2.9 GB\n"
                "☁️ Mis en ligne sur : Google Drive\n"
                "🔐 Mot de passe : MobiFirmware.VIP\n"
                "━━━━━━━━━━━━\n"
                "✨ Dump complet prêt pour les techniciens\n"
                "HMAX hithamMax\n"
            )
            btn_download = "📥 Télécharger - Google Drive 2.9GB"
            btn_back = "⬅️ Retour"
        else:  # ar هو الافتراضي
            txt = (
                "🌟 اليوم بنقدم لكم دامب جديد ومهم 🌟\n"
                "━━━━━━━━━━━━\n"
                "📱 Motorola XT2523-7\n"
                "🔥 Moto E15 5G\n"
                "💾 FULL DUMP\n"
                "🔧 Pulled By: AMT TOOL\n"
                "📦 Dump Size: 2.9 GB\n"
                "☁️ Uploaded To: Google Drive\n"
                "🔐 Pass File: MobiFirmware.VIP\n"
                "━━━━━━━━━━━━\n"
                "✨ دامب كامل جاهز لخدمة الفنيين\n"
                "HMAX hithamMax\n"
            )
            btn_download = "📥 Download - Google Drive 2.9GB"
            btn_back = "⬅️ Back"
        markup.add(types.InlineKeyboardButton(btn_download, url=gdrive_url))
        markup.add(types.InlineKeyboardButton(btn_back, callback_data="dump_motorola_section"))
        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(call.message.chat.id, photo, caption=txt, reply_markup=markup)
        except Exception as e:
            print(f"Send Motorola E15 photo failed: {e}")
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    elif cd == "dump_jtag_f64_ultra_section":
        markup = types.InlineKeyboardMarkup(row_width=1)
        txt = _dump_localize(user_id, "🛠️ *DUMP Via F64 ULTRA JTAG*\n\nAll dumps dumped with F64 ULTRA:")
        for model, callback in DUMP_SMART_SECTIONS["jtag"]:
            markup.add(types.InlineKeyboardButton(model, callback_data=callback))
        markup.add(types.InlineKeyboardButton(_dump_back_label(user_id, "🔙 Back"), callback_data="f64_ultra_dump_section"))
        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass
        _hmax_show_menu(call, txt, markup, parse_mode="Markdown")
        return

    elif cd in (
        "dump_xiaomi_group_section",
        "dump_redmi_section",
        "dump_xiaomi_section",
        "dump_poco_section",
        "dump_redmi_old_section",
        "dump_xiaomi_redmi_poco_section",
    ):
        markup = types.InlineKeyboardMarkup(row_width=1)
        txt = _dump_localize(user_id, "📱 *XIAOMI | REDMI | POCO*\nOne Company - All Models\n\nSelect model:")
        for model, callback in DUMP_SMART_SECTIONS["xiaomi_group"]:
            markup.add(types.InlineKeyboardButton(model, callback_data=callback))
        markup.add(types.InlineKeyboardButton("🔙 Back", callback_data="dump_main_section"))
        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass
        _hmax_show_menu(call, txt, markup, parse_mode="Markdown")
        return

    elif cd in ("dump_oppo_section", "dump_oppo_full_section"):
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "🔥 A55 CPH2325 F.71 FULL 4.7GB [PANDORA]"), callback_data="dump_model_oppo_a55_cph2325_f71"))
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "🔥 CPH1933 A5 2020 - FULL DUMP 3GB [Pandora]"), callback_data="dump_model_oppo_cph1933_a5_2020_full_dump_pandora"))
        for model, callback in DUMP_SMART_SECTIONS["oppo"]:
            markup.add(types.InlineKeyboardButton(model, callback_data=callback))
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "⬅️ Back to DUMP"), callback_data="dump_main_section"))
        section_text = (
            "📱 OPPO - Official Firmware Library\n"
            "━━━━━━━━━━━━\n"
            "🔷 Brand: OPPO\n"
            "📦 FULL DUMP Library\n"
            "☁️ Google Drive\n"
            "━━━━━━━━━━━━\n"
            "اختر الموديل:"
        )
        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass
        _hmax_show_menu(call, _dump_localize(user_id, section_text), markup)
        return

    elif cd == "dump_model_oppo_a55_cph2325_f71":
        markup = types.InlineKeyboardMarkup(row_width=1)
        gdrive_url = "https://drive.google.com/file/d/1KsSxwMJRtAJoAGeTA7Uq4JHgzbe2GsMz/view"
        photo_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "images",
            "oppo_a55_cph2325_f71_full_dump_4_7gb_pandora_arabic.jpg",
        )
        try:
            bot.answer_callback_query(call.id)
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except:
            pass
        txt = (
            "📱 OPPO A55 — CPH2325 — FULL DUMP 🔥\n"
            "━━━━━━━━━━━━\n"
            "⚠️ القصة:\n"
            "جهاز اتفَلّش بدامب قديم موجود بالجروب...\n"
            "والنتيجة؟ الهاتف مات 💀\n"
            "━━━━━━━━━━━━\n"
            "👤 التجربة بواسطة:\n"
            "محمد محمود الشرقية\n"
            "━━━━━━━━━━━━\n"
            "🔥 الإصدار الأصلي على الجهاز:\n"
            "CPH2325_11_F.75\n"
            "━━━━━━━━━━━━\n"
            "❌ الدامب المجرب:\n"
            "OPPO_CPH2325_11_F.71_DUMP BY PANDORA TOOL\n"
            "النتيجة: الهاتف مات\n"
            "━━━━━━━━━━━━\n"
            "✅ الإصدار اللي حل المشكلة:\n"
            "CPH2325_11_F.67 - تم الحل ✅\n"
            "━━━━━━━━━━━━\n"
            "📌 الخلاصة والنصيحة الذهبية:\n"
            "قبل ما تبدأ التفليش، اعرف إصدار الجهاز كويس،\n"
            "وخد ملفات الشبكة، وحاول تختار نفس الإصدار\n"
            "أو إصدار قريب منه قدر الإمكان.\n"
            "━━━━━━━━━━━━\n"
            "📱 Device: OPPO A55 CPH2325\n"
            "📦 File: CPH2325 11 F.71 FULL DUMP\n"
            "🔧 Tool: PANDORA TOOL\n"
            "📦 Size: 4.7 GB\n"
            "☁️ Hosting: Google Drive\n"
            "🔐 Pass: MobiFirmware.VIP\n"
        )
        txt = _dump_card_text(user_id, "dump_model_oppo_a55_cph2325_f71", txt)
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📥 Download 4.7GB - Google Drive"), url=gdrive_url))
        markup.add(types.InlineKeyboardButton(_dump_back_label(user_id, "⬅️ Back"), callback_data="dump_oppo_section"))
        try:
            with open(photo_path, 'rb') as photo:
                bot.send_photo(call.message.chat.id, photo, caption=txt, reply_markup=markup)
        except Exception as e:
            print(f"Photo error: {e}")
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    elif cd == "dump_model_oppo_cph1933_a5_2020_full_dump_pandora":
        markup = types.InlineKeyboardMarkup(row_width=1)
        gdrive_url = "https://drive.google.com/file/d/1xQjwapIINwF4rewMG38Sd7n1iltoqep2/view"
        photo_path = "images/oppo_cph1933_a5_2020_full_dump_pandora.jpg"
        try:
            bot.answer_callback_query(call.id)
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except: pass
        txt = (
            "🔥 OPPO CPH1933 (A5 2020) — FULL DUMP 🔥\n"
            "━━━━━━━━━━━━\n"
            "📱 Device: OPPO A5 2020\n"
            "📋 Model: CPH1933\n"
            "🔧 Dump Tool: Pandora Tool\n"
            "📦 Dump Size: 3 GB\n"
            "☁️ Uploaded on: Google Drive\n"
            "👤 بناءً على طلب العضو: Ahmed EL-Melwany\n"
            "🔐 Pass File: MobiFirmware.VIP\n"
            "━━━━━━━━━━━━\n"
            "📊 بيانات الدامب\n"
            "OEM PK HASH: 6E91B529AAD0307F1FC67310DAB1FF821EB7AA02FA5620157A9D20E124F4E0B84897B1389836216B4F2CB50D8DBB87B8\n"
            "CPU: SM6125 (Snapdragon 665)\n"
            "Vendor: OPPO\n"
            "MSM HW ID: 0010A0E100510000\n"
            "SBL SW Ver: 00000001\n"
            "Product Brand: qti\n"
            "Manufacturer: QUALCOMM\n"
            "Product Model: OPPO A5 2020\n"
            "Product Name: qssi\n"
            "Product Device: qssi\n"
            "Product Board: trinket\n"
            "Board Platform: trinket\n"
            "Build ID: RKQ1.200903.002\n"
            "Build Date: Sat Sep 3 22:41:12 CST 2022\n"
            "Display ID: CPH1933_11_F.01\n"
            "Security Patch: 2022-09-05\n"
            "Version SDK: 30\n"
            "Version Release: 11\n"
            "Version Codename: REL\n"
            "Firmware Version: 1662212765538\n"
            "Userdata FS Type: EXT4\n"
            "━━━━━━━━━━━━\n"
            "⚠️ مهم للفنيين: تأكد من مطابقة بيانات الجهاز والإصدار قبل التفليش، ويفضل دائمًا أخذ Backup لملفات الشبكة قبل البدء\n"
            "━━━━━━━━━━━━\n"
            "HMAX hithamMax\n"
        )
        txt = _dump_card_text(user_id, "dump_model_oppo_cph1933_a5_2020_full_dump_pandora", txt)
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📥 Download - Google Drive 3GB"), url=gdrive_url))
        markup.add(types.InlineKeyboardButton(_dump_back_label(user_id, "⬅️ Back"), callback_data="dump_oppo_section"))
        try:
            with open(photo_path, 'rb') as photo:
                bot.send_photo(call.message.chat.id, photo, caption=txt, reply_markup=markup)
        except Exception as e:
            print(f"Photo error: {e}")
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    elif cd in (
        "dump_infinix_full_section",
        "dump_vivo_full_section",
    ):
        lang = hmaxi18n.get_language(user_id)
        brand = {
            "dump_infinix_full_section": "INFINIX",
            "dump_vivo_full_section": "VIVO",
        }[cd]
        markup = types.InlineKeyboardMarkup(row_width=1)
        txt = _dump_localize(user_id, f"📱 *{brand}*\n\nSelect model:")
        btn_back = "🔙 Back"
        if brand == "VIVO":
            if lang == "en":
                txt = "📱 *VIVO*\n\nSelect model:"
                empty_text = "📱 *VIVO*\n\nNo dump files are available yet."
                btn_back = "🔙 Back"
                y03_label = "🔥 Y03 Dump File 4GB [JTAG]"
                y04_label = "🔥 Y04 V2430 Latest Dump 10GB [JTAG]"
                y04_2_label = "🔥 Y04 V2430 (2) OSv15 Dump 5GB [JTAG]"
                y27_label = "🔥 Y27 & Y36 5G V2248 - Full Dump 7.3GB [RARE]"
            elif lang == "fr":
                txt = "📱 *VIVO*\n\nSélectionner le modèle :"
                empty_text = "📱 *VIVO*\n\nAucun fichier dump n’est disponible pour le moment."
                btn_back = "🔙 Retour"
                y03_label = "🔥 Y03 - Fichier dump 4GB [JTAG]"
                y04_label = "🔥 Y04 V2430 - Dernier dump 10GB [JTAG]"
                y04_2_label = "🔥 Y04 V2430 (2) - Dump OSv15 5GB [JTAG]"
                y27_label = "🔥 Y27 & Y36 5G V2248 - Dump complet 7.3GB [RARE]"
            else:
                txt = "📱 *VIVO*\n\nاختر الموديل:"
                empty_text = "📱 *VIVO*\n\nلا توجد ملفات دامب متاحة حالياً."
                btn_back = "🔙 رجوع"
                y03_label = "🔥 Y03 - ملف دامب 4GB [JTAG]"
                y04_label = "🔥 Y04 V2430 - أحدث دامب 10GB [JTAG]"
                y04_2_label = "🔥 Y04 V2430 (2) - دامب OSv15 5GB [JTAG]"
                y27_label = "🔥 Y27 & Y36 5G V2248 - دامب كامل 7.3GB [نادر]"
        available_models = DUMP_SMART_SECTIONS.get(brand.lower(), [])
        for model, callback in available_models:
            if brand == "VIVO":
                if callback == "dump_model_vivo_y03_dump_4gb":
                    model = y03_label
                elif callback == "dump_model_vivo_y04_v2430_latest":
                    model = y04_label
                elif callback == "dump_model_vivo_y04_v2430_2_osv15_easyjtag":
                    model = y04_2_label
                elif callback == "dump_model_vivo_y27_y36_5g_v2248_pd2279f_ex_a_15_2_10_2_w20":
                    model = y27_label
                elif callback in VIVO_UNLOCKTOOL_DUMPS:
                    model = VIVO_UNLOCKTOOL_DUMPS[callback]["menu"].get(
                        lang,
                        VIVO_UNLOCKTOOL_DUMPS[callback]["menu"]["ar"],
                    )
            markup.add(types.InlineKeyboardButton(model, callback_data=callback))
        if not available_models:
            if brand == "VIVO":
                txt = empty_text
            else:
                txt = f"📱 *{brand}*\n\nNo dump files are available yet."
        markup.add(types.InlineKeyboardButton(btn_back, callback_data="dump_main_section"))
        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass
        _hmax_show_menu(call, txt, markup, parse_mode="Markdown")
        return

    elif cd == "dump_model_infinix_x657c_smart5":
        markup = types.InlineKeyboardMarkup(row_width=1)
        photo_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "images",
            "infinix_smart5_x657c_full_nv_dump.jpg",
        )
        try:
            bot.answer_callback_query(call.id)
        except Exception as e:
            print(f"Answer Infinix Smart 5 callback failed: {e}")
        try:
            bot.delete_message(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
            )
        except Exception as e:
            print(f"Delete Infinix Smart 5 menu failed: {e}")

        txt = (
            "📱 Infinix Smart 5 - X657C - Full Dump + NV 📱\n"
            "━━━━━━━━━━━━\n"
            "🏷️ Model: X657C - Smart 5\n"
            "🔖 Firmware: X657C-H6117GH-QGo-GL-210825V252\n"
            "📦 Type: Full Dump File + NV File\n"
            "🔧 Tool: Unlock Tool\n"
            "📦 Size: 1.6GB\n"
            "━━━━━━━━━━━━\n"
            "📱 Specs: 6.6 IPS LCD 720x1600\n"
            "🔧 Helio A20 - RAM 2/3GB - 32/64GB\n"
            "📸 13MP - 5000mAh\n"
            "━━━━━━━━━━━━\n"
            "☁️ Google Drive\n"
            "🔐 Pass: MobiFirmware.VIP\n"
        )
        txt = _dump_card_text(user_id, "dump_model_infinix_x657c_smart5", txt)
        markup.add(types.InlineKeyboardButton(
            _dump_btn(user_id, "📥 Download 1.6GB - Google Drive"),
            url="https://drive.google.com/file/d/148UbsVqN_G7H2OsJlPH5-S6kGr3YfJ-C/view",
        ))
        markup.add(types.InlineKeyboardButton(
            _dump_back_label(user_id, "⬅️ Back"),
            callback_data="dump_infinix_full_section",
        ))
        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(
                    call.message.chat.id,
                    photo,
                    caption=txt,
                    reply_markup=markup,
                )
        except Exception as e:
            print(f"Send Infinix Smart 5 photo failed: {e}")
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    elif cd == "dump_model_infinix_note_30_5g_x6711_v600":
        markup = types.InlineKeyboardMarkup(row_width=1)
        gdrive_url = "https://drive.google.com/file/d/1ubef2yjzrQpNB0MFPw8UWdraxPr6OtbB/view"
        photo_path = "images/infinix_note_30_5g_x6711_v600.jpg"
        try:
            bot.answer_callback_query(call.id)
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except:
            pass
        txt = (
            "📱 INFINIX NOTE 30 5G - FULL DUMP 📱\n"
            "━━━━━━━━━━━━\n"
            "📱 Device: INFINIX NOTE 30 5G\n"
            "🏷️ Model: X6711 - V600\n"
            "📁 File: FULL DUMP\n"
            "🔧 Pulled By: Pandora Tool\n"
            "━━━━━━━━━━━━\n"
            "🔐 Pass: MobiFirmware.VIP\n"
        )
        txt = _dump_card_text(user_id, "dump_model_infinix_note_30_5g_x6711_v600", txt)
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📥 Download - Google Drive"), url=gdrive_url))
        markup.add(types.InlineKeyboardButton(_dump_back_label(user_id, "⬅️ Back"), callback_data="dump_infinix_full_section"))
        try:
            with open(photo_path, 'rb') as photo:
                bot.send_photo(call.message.chat.id, photo, caption=txt, reply_markup=markup)
        except:
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    # ===== قسم Infinix =====
    elif cd == "dump_infinix_section":
        BRAND_INF = "Infini" + "x"  # عشان ما يطلع تاق
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton(f"🔥 {BRAND_INF} Smart 6 X6511B - Factory Signed", callback_data="dump_model_x6511b_factory_signed"))
        markup.add(types.InlineKeyboardButton(f"🔥 {BRAND_INF} Smart 20 X6840B - FULL DUMP", callback_data="dump_model_x6840b_full_dump"))
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "⬅️ Back to DUMP"), callback_data="dump_main_section"))
        try:
            bot.edit_message_text(_dump_localize(user_id, f"📱 {BRAND_INF} - Firmware Library\nاختر الموديل:"), call.message.chat.id, call.message.message_id, reply_markup=markup)
        except:
            bot.send_message(call.message.chat.id, f"📱 {BRAND_INF} Section", reply_markup=markup)

    elif cd == "dump_model_x6840b_full_dump":
        BRAND_INF = "Infini" + "x"
        DUMP_TOOL = "UnlockTool"
        markup = types.InlineKeyboardMarkup(row_width=1)
        gdrive_url = "https://drive.google.com/file/d/1AZywXmJEL1BBJaB3Cx5KF7iE7G3c2RqS/view"
        photo_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "images",
            "infinix_smart20_x6840b_dump_hmax.jpg",
        )
        try:
            bot.answer_callback_query(call.id)
        except Exception as e:
            print(f"Answer Smart 20 callback failed: {e}")
        try:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except Exception as e:
            print(f"Delete Smart 20 menu failed: {e}")
        txt = (
            "🔥 Smart 20 — X6840B — FULL DUMP 🔥\n"
            "━━━━━━━━━━━━\n"
            "📱 DEVICE INFO:\n"
            "• Model: Smart 20\n"
            "• Model No.: X6840B\n"
            "• Firmware: 16.1.0.150SP02\n"
            "• Build ID: OP001PF001AZ\n"
            "━━━━━━━━━━━━\n"
            "📂 FILE INFO:\n"
            "• File Type: FULL DUMP\n"
            "• Dump Status: READBACK FROM DEVICE\n"
            f"• Dump Tool: {DUMP_TOOL}\n"
            "• Purpose: Software Service / Flashing\n"
            "━━━━━━━━━━━━\n"
            "🔧 SERVICE NOTES:\n"
            "• مناسب للعمل على نفس Model & Build\n"
            f"• تم سحب الدامب باستخدام {DUMP_TOOL}\n"
            "• ينصح باستخدامه كمرجع مطابق لنفس الاصدار\n"
            "━━━━━━━━━━━━\n"
            "⚠️ IMPORTANT - قبل التفليش:\n"
            "• خذ Full Backup من الجهاز الاصلي\n"
            "• اسحب Network / Calibration Files واحتفظ بنسخة\n"
            "• تأكد من مطابقة Model + Build قبل البدء\n"
            "━━━━━━━━━━━━\n"
            "🔐 Password: MobiFirmware.VIP\n"
            "☁️ Host: Google Drive\n"
            "━━━━━━━━━━━━\n"
            "HMAX-UNLOCKER - HithamMax\n"
        )
        txt = _dump_card_text(user_id, "dump_model_x6840b_full_dump", txt)
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📥 Download - Google Drive"), url=gdrive_url))
        markup.add(types.InlineKeyboardButton(f"⬅️ Back to {BRAND_INF}", callback_data="dump_infinix_section"))
        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(call.message.chat.id, photo, caption=txt, reply_markup=markup)
        except Exception as e:
            print(f"Send Smart 20 photo failed: {e}")
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    elif cd == "dump_model_x6511b_factory_signed":
        BRAND_INF = "Infini" + "x"
        markup = types.InlineKeyboardMarkup(row_width=1)
        gdrive_url = "https://drive.google.com/file/d/1LpISua-lTGlvea_P5oR9alxyEHTVuzcR/view"
        photo_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "images",
            "infinix_smart6_x6511b_factory_hmax.jpg",
        )
        try:
            bot.answer_callback_query(call.id)
        except Exception as e:
            print(f"Answer Smart 6 callback failed: {e}")
        try:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except Exception as e:
            print(f"Delete Smart 6 menu failed: {e}")
        txt = (
            f"🔥 {BRAND_INF} Smart 6 — X6511B — Factory Signed 🔥\n"
            "━━━━━━━━━━━━\n"
            "💎 إصدار الفلاشة:\n"
            "X6511B-F6318-11.0-OP-V127-20230810\n"
            "━━━━━━━━━━━━\n"
            "✅ Factory Signed Firmware\n"
            "• Verified • Official • Secure\n"
            "🔨 فلاشة مصنعية مجربة 100%\n"
            "━━━━━━━━━━━━\n"
            "🎁 الفلاشة مدفوعة في جميع المواقع\n"
            "🎁 ومتاحة الآن مجاناً\n"
            "━━━━━━━━━━━━\n"
            "🔐 كلمة مرور الفلاشة: MobiFirmware.VIP\n"
            "☁️ التحميل عبر Google Drive\n"
            "━━━━━━━━━━━━\n"
            "📦 مواصفات الهاتف:\n"
            "• شاشة 6.6 HD+ \n"
            "• معالج Unisoc SC9863A Octa-Core\n"
            "• RAM: 2GB - ذاكرة 32GB\n"
            "• كاميرا خلفية 8MP - امامية 5MP\n"
            "• بطارية 5000mAh - Android 11 Go\n"
            "• 4G LTE - بصمة خلفية - Micro-USB\n"
            "━━━━━━━━━━━━\n"
            "HMAX-UNLOCKER - HithamMax\n"
        )
        txt = _dump_card_text(user_id, "dump_model_x6511b_factory_signed", txt)
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📥 Download - Google Drive"), url=gdrive_url))
        markup.add(types.InlineKeyboardButton(f"⬅️ Back to {BRAND_INF}", callback_data="dump_infinix_section"))
        try:
            with open(photo_path, 'rb') as photo:
                bot.send_photo(call.message.chat.id, photo, caption=txt, reply_markup=markup)
        except Exception as e:
            print(f"Photo error: {e}")
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return


    elif cd == "dump_model_oppo_a6_pro_5g_cph2781":
        markup = types.InlineKeyboardMarkup(row_width=1)
        gdrive_url = "https://drive.google.com/file/d/1cW5EhSPHntwe3W3tiDN651OpvXvf7gHJ/view"
        photo_path = "images/oppo_a6_pro_5g_cph2781.jpg"
        try:
            bot.answer_callback_query(call.id)
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except:
            pass
        txt = (
            "📱 OPPO A6 PRO 5G - DUMP FILE 📱\n"
            "━━━━━━━━━━━━\n"
            "📱 Device: OPPO A6 PRO 5G\n"
            "🏷️ Model: CPH2781_11.A.31\n"
            "💾 Storage: UFS 128GB\n"
            "🔧 Pulled By: F64 BOX\n"
            "☁️ Upload: Google Drive\n"
            "━━━━━━━━━━━━\n"
            "🔐 Pass: MobiFirmware.VIP\n"
        )
        txt = _dump_card_text(user_id, "dump_model_oppo_a6_pro_5g_cph2781", txt)
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📥 Download - Google Drive"), url=gdrive_url))
        markup.add(types.InlineKeyboardButton(_dump_back_label(user_id, "⬅️ Back"), callback_data="dump_oppo_full_section"))
        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(call.message.chat.id, photo, caption=txt, reply_markup=markup)
        except:
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    elif cd == "dump_model_oppo_a54_cph2239_dead_boot":
        markup = types.InlineKeyboardMarkup(row_width=1)
        gdrive_url = "https://drive.google.com/file/d/1-J8LMb2OzTHZXJl0M8Y4pE6A6uNrREg1/view"
        photo_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "images",
            "oppo_a54_cph2239_dead_boot.jpg",
        )
        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass
        try:
            bot.delete_message(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
            )
        except Exception as e:
            print(f"Delete OPPO A54 menu failed: {e}")

        txt = (
            "📱 OPPO A54 - Dead Boot Repair 📱\n"
            "━━━━━━━━━━━━\n"
            "📱 Device: OPPO A54\n"
            "🏷️ Model: CPH2239_11_C.33 [Dead Boot Repair]\n"
            "🔧 Tool: Unlock Tool\n"
            "📦 File: Full dump + Nv file\n"
            "☁️ Upload: Google Drive\n"
            "━━━━━━━━━━━━\n"
            "🔐 Pass: MobiFirmware.VIP"
        )
        txt = _dump_card_text(user_id, "dump_model_oppo_a54_cph2239_dead_boot", txt)
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📥 Download - Google Drive"), url=gdrive_url))
        markup.add(types.InlineKeyboardButton(_dump_back_label(user_id, "⬅️ Back"), callback_data="dump_oppo_full_section"))
        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(
                    call.message.chat.id,
                    photo,
                    caption=txt,
                    reply_markup=markup,
                )
        except Exception as e:
            print(f"Send OPPO A54 photo failed: {e}")
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    elif cd == "dump_model_oppo_a31_cph2015_128gb":
        markup = types.InlineKeyboardMarkup(row_width=1)
        gdrive_url = "https://drive.google.com/file/d/1ZJ6o9C8jFB9MeRHdnB1N-AkeGtpaBu64/view"
        photo_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "images",
            "oppo_a31_cph2015_128gb_emmc_dump.jpg",
        )
        try:
            bot.answer_callback_query(call.id)
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except Exception:
            pass
        txt = (
            "🔥 NEW DUMP RELEASE 🔥\n"
            "━━━━━━━━━━━━\n"
            "📱 OPPO A31 — CPH2015\n"
            "💾 128GB eMMC DUMP\n"
            "🔧 Pulled by EASY JTAG PLUS\n"
            "📦 Size: 2.4 GB\n"
            "☁️ Google Drive Upload\n"
            "🔐 Pass: MobiFirmware.VIP\n"
            "━━━━━━━━━━━━\n"
            "📋 Device: OPPO A31 CPH2015\n"
            "File: 128GB eMMC DUMP\n"
            "Pulled By: EASY JTAG PLUS\n"
            "Upload: Google Drive\n"
            "━━━━━━━━━━━━\n"
            "HMAX hithamMax - PROFESSIONAL FIRMWARE SOLUTIONS\n"
        )
        txt = _dump_card_text(user_id, "dump_model_oppo_a31_cph2015_128gb", txt)
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📥 Download - Google Drive 2.4GB"), url=gdrive_url))
        markup.add(types.InlineKeyboardButton(_dump_back_label(user_id, "⬅️ Back"), callback_data="dump_oppo_section"))
        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(call.message.chat.id, photo, caption=txt, reply_markup=markup)
        except Exception as e:
            print(f"Photo error: {e}")
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    elif cd == "dump_model_oppo_a57_cph2387":
        markup = types.InlineKeyboardMarkup(row_width=1)
        gdrive_url = "https://drive.google.com/file/d/1iVZkaOdBacWxZEjxenBhqYJxldSBqN3i/view"
        try:
            bot.answer_callback_query(call.id)
        except:
            pass
        try:
            bot.delete_message(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
            )
        except:
            pass

        txt = (
            "🔥 OPPO A57 CPH2387 DUMP FILE 🔥\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "📱 Model: OPPO A57 CPH2387\n"
            "🛠️ Dump File By: EASY JTAG PLUS\n"
            "👤 Uploaded By: Reynold Bermil Leonido\n"
            "🔐 Password: MobiFirmware.VIP\n"
            "📅 Uploaded: Oct 2025\n"
            "📂 Format: BIN • DUMP • FULL\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "✅ Verified • Safe • Ready\n"
            "📞 https://wa.me/message/A3KQWHSSERCFG1\n"
        )
        txt = _dump_card_text(user_id, "dump_model_oppo_a57_cph2387", txt)
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📥 Download - Google Drive"), url=gdrive_url))
        markup.add(types.InlineKeyboardButton(_dump_back_label(user_id, "🔙 Back"), callback_data="dump_oppo_full_section"))
        bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    elif cd == "dump_model_oppo_reno_12f_4g_cph2687":
        markup = types.InlineKeyboardMarkup(row_width=1)
        gdrive_url = "https://drive.google.com/file/d/1OY4I_TmBJsEKNlUdHPULjpiLOEyQJuIc/view"
        photo_path = "images/oppo_reno_12f_4g_cph2687.jpg"
        try:
            bot.answer_callback_query(call.id)
            bot.delete_message(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
            )
        except:
            pass
        txt = (
            "📱 OPPO RENO 12F 4G - DUMP FILE 📱\n"
            "━━━━━━━━━━━━\n"
            "🏷️ Model: CPH2687\n"
            "🛠️ Dump By: F64 BOX\n"
            "📦 Dump Type: Full Flash / Userdata / Boot / Recovery\n"
            "🧠 Chipset: MediaTek Helio G99\n"
            "💾 Memory: 8GB RAM • 256GB Storage\n"
            "📏 Dump Size: 8.52 GB\n"
            "📅 Date: 2024-06-12 18:42 UTC\n"
            "📁 File: CPH2687_F64BOX_FullDump_20240612.zip\n"
            "━━━━━━━━━━━━\n"
            "🔐 Pass: MobiFirmware.VIP\n"
        )
        txt = _dump_card_text(user_id, "dump_model_oppo_reno_12f_4g_cph2687", txt)
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📥 Download - Google Drive"), url=gdrive_url))
        markup.add(types.InlineKeyboardButton(_dump_back_label(user_id, "⬅️ Back"), callback_data="dump_oppo_full_section"))
        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(call.message.chat.id, photo, caption=txt, reply_markup=markup)
        except:
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return


    elif cd in (
        "dump_model_vivo_y20s_g_y12s_fake_8_256",
        "dump_model_vivo_y12s_v2026_pd2036f",
        "dump_model_vivo_y100_v2239_pd2257f",
        "dump_model_vivo_y53s_v2058_pd2103f",
        "dump_model_vivo_y75a",
        "dump_model_vivo_y21_pd2139f",
        "dump_model_vivo_v27e_v2237",
        "dump_model_vivo_y02s_v2203_pd2216f",
        "dump_model_vivo_y1s_pd2014f",
        "dump_model_vivo_y83_pd1803bf",
    ):
        # One data-driven card renderer keeps all supplied VIVO UnlockTool
        # resources consistent while preserving a localized caption and menu.
        lang = hmaxi18n.get_language(user_id)
        vivo_dump = VIVO_UNLOCKTOOL_DUMPS[cd]
        photo_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "images",
            vivo_dump["poster"],
        )
        button_labels = {
            "ar": {
                "download": "📥 تحميل الملف — Google Drive",
                "back": "⬅️ رجوع إلى VIVO",
            },
            "en": {
                "download": "📥 Download file — Google Drive",
                "back": "⬅️ Back to VIVO",
            },
            "fr": {
                "download": "📥 Télécharger — Google Drive",
                "back": "⬅️ Retour à VIVO",
            },
        }.get(lang, {})
        if not button_labels:
            button_labels = {
                "download": "📥 تحميل الملف — Google Drive",
                "back": "⬅️ رجوع إلى VIVO",
            }

        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass
        try:
            bot.delete_message(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
            )
        except Exception:
            pass

        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton(
                button_labels["download"],
                url=vivo_dump["url"],
            )
        )
        markup.add(
            types.InlineKeyboardButton(
                button_labels["back"],
                callback_data="dump_vivo_full_section",
            )
        )
        caption = vivo_unlocktool_dump_caption(vivo_dump, lang)
        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(
                    call.message.chat.id,
                    photo,
                    caption=caption,
                    reply_markup=markup,
                )
        except Exception as error:
            print(f"Send VIVO UnlockTool poster failed: {error}")
            bot.send_message(
                call.message.chat.id,
                caption,
                reply_markup=markup,
            )
        return

    elif cd == "dump_model_vivo_y03_dump_4gb":
        lang = hmaxi18n.get_language(user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        gdrive_url = "https://drive.google.com/file/d/1yWmS6BEQYLtaNQmNJ_VgP6ojqMm66dak/view"
        photo_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "images",
            "vivo_y03_dump_4gb_easy_jtag.jpg",
        )

        try:
            bot.answer_callback_query(call.id)
        except Exception as e:
            print(f"Answer VIVO Y03 callback failed: {e}")
        try:
            bot.delete_message(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
            )
        except Exception as e:
            print(f"Delete VIVO Y03 menu failed: {e}")

        if lang == "en":
            txt = (
                "📱 VIVO Y03 - DUMP FILE 🔥\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                "📱 Device: VIVO Y03\n"
                "📦 Type: VIVO Y03 dump file\n"
                "🔧 Dumped with: EASY JTAG PLUS\n"
                "📦 Dump size: 4.0 GB\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                "☁️ Upload server: Google Drive\n"
                "🔐 File password: MobiFirmware.VIP"
            )
            btn_download = "📥 Download 4GB - Google Drive"
            btn_back = "⬅️ Back"
        elif lang == "fr":
            txt = (
                "📱 VIVO Y03 - FICHIER DUMP 🔥\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                "📱 Appareil : VIVO Y03\n"
                "📦 Type : Fichier dump VIVO Y03\n"
                "🔧 Extrait avec : EASY JTAG PLUS\n"
                "📦 Taille du dump : 4.0 GB\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                "☁️ Serveur de téléchargement : Google Drive\n"
                "🔐 Mot de passe du fichier : MobiFirmware.VIP"
            )
            btn_download = "📥 Télécharger 4GB - Google Drive"
            btn_back = "⬅️ Retour"
        else:
            txt = (
                "📱 VIVO Y03 - ملف دامب 🔥\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                "📱 الجهاز: VIVO Y03\n"
                "📦 النوع: ملف دامب VIVO Y03\n"
                "🔧 تم السحب بواسطة: EASY JTAG PLUS\n"
                "📦 حجم الدامب: 4.0 GB\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                "☁️ سيرفر الرفع: Google Drive\n"
                "🔐 كلمة مرور الملف: MobiFirmware.VIP"
            )
            btn_download = "📥 تحميل 4GB - Google Drive"
            btn_back = "⬅️ رجوع"

        markup.add(types.InlineKeyboardButton(btn_download, url=gdrive_url))
        markup.add(types.InlineKeyboardButton(
            btn_back,
            callback_data="dump_vivo_full_section",
        ))
        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(
                    call.message.chat.id,
                    photo,
                    caption=txt,
                    reply_markup=markup,
                )
        except Exception as e:
            print(f"Send VIVO Y03 photo failed: {e}")
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    elif cd == "dump_model_vivo_y04_v2430_latest":
        lang = hmaxi18n.get_language(user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        gdrive_url = "https://drive.google.com/file/d/1ES_gWuEgOgGK9Yq-8ugriHPPjYIEtot_/view"
        photo_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "images",
            "vivo_y04_v2430_latest_10gb_jtag_mustafa.jpg",
        )

        try:
            bot.answer_callback_query(call.id)
        except Exception as e:
            print(f"Answer VIVO Y04 callback failed: {e}")
        try:
            bot.delete_message(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
            )
        except Exception as e:
            print(f"Delete VIVO Y04 menu failed: {e}")

        if lang == "en":
            txt = (
                "📱 VIVO Y04 V2430 - Latest Version Dump 🔥\n"
                "━━━━━━━━━━━━\n"
                "📱 Device: VIVO Y04\n"
                "🏷️ Model: V2430\n"
                "📦 Type: Latest version dump\n"
                "🔧 Tool: EASY JTAG PLUS\n"
                "📦 Dump size: 10 GB\n"
                "━━━━━━━━━━━━\n"
                "☁️ File hosting: Google Drive\n"
                "🔐 File password: MobiFirmware.VIP\n"
                "━━━━━━━━━━━━\n"
                "🙏 Special thanks to engineer Mustafa Saied\n"
                "for extracting and uploading the dump."
            )
            btn_download = "📥 Download 10GB - Google Drive"
            btn_back = "⬅️ Back"
        elif lang == "fr":
            txt = (
                "📱 VIVO Y04 V2430 - Dump dernière version 🔥\n"
                "━━━━━━━━━━━━\n"
                "📱 Appareil : VIVO Y04\n"
                "🏷️ Modèle : V2430\n"
                "📦 Type : Dump de la dernière version\n"
                "🔧 Outil : EASY JTAG PLUS\n"
                "📦 Taille du dump : 10 GB\n"
                "━━━━━━━━━━━━\n"
                "☁️ Hébergement : Google Drive\n"
                "🔐 Mot de passe du fichier : MobiFirmware.VIP\n"
                "━━━━━━━━━━━━\n"
                "🙏 Un grand merci à l’ingénieur Mustafa Saied\n"
                "pour l’extraction et le téléversement du dump."
            )
            btn_download = "📥 Télécharger 10GB - Google Drive"
            btn_back = "⬅️ Retour"
        else:
            txt = (
                "📱 VIVO Y04 V2430 - دامب آخر إصدار 🔥\n"
                "━━━━━━━━━━━━\n"
                "📱 الجهاز: VIVO Y04\n"
                "🏷️ الموديل: V2430\n"
                "📦 النوع: دامب آخر إصدار\n"
                "🔧 الأداة: EASY JTAG PLUS\n"
                "📦 حجم الدامب: 10 GB\n"
                "━━━━━━━━━━━━\n"
                "☁️ الاستضافة: Google Drive\n"
                "🔐 كلمة مرور الملف: MobiFirmware.VIP\n"
                "━━━━━━━━━━━━\n"
                "🙏 كل الشكر والتقدير للمهندس مصطفى سعيد\n"
                "على سحب الدامب ورفعه."
            )
            btn_download = "📥 تحميل 10GB - Google Drive"
            btn_back = "⬅️ رجوع"

        markup.add(types.InlineKeyboardButton(btn_download, url=gdrive_url))
        markup.add(types.InlineKeyboardButton(
            btn_back,
            callback_data="dump_vivo_full_section",
        ))
        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(
                    call.message.chat.id,
                    photo,
                    caption=txt,
                    reply_markup=markup,
                )
        except Exception as e:
            print(f"Send VIVO Y04 photo failed: {e}")
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    elif cd == "dump_model_vivo_y04_v2430_2_osv15_easyjtag":
        lang = hmaxi18n.get_language(user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        gdrive_url = "https://drive.google.com/file/d/1d1cUndyviNVH2ML2xgaAlgJUaCf3wGpT/view"
        photo_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "images",
            "vivo_y04_v2430_2_osv15_easyjtag_khaled_kabo.jpg",
        )

        try:
            bot.answer_callback_query(call.id)
        except Exception as e:
            print(f"Answer VIVO Y04 (2) callback failed: {e}")
        try:
            bot.delete_message(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
            )
        except Exception as e:
            print(f"Delete VIVO Y04 (2) menu failed: {e}")

        if lang == "en":
            txt = (
                "🔥 (2) VIVO Y04 — V2430 — OSv15 DUMP 🔥\n"
                "━━━━━━━━━━━━\n"
                "⚙️ Requested by a group member\n"
                "👤 ĶĦălěď Ķäbô ❤️\n"
                "━━━━━━━━━━━━\n"
                "📱 VIVO Y04 — V2430\n"
                "⚡ OSv15 DUMP | BY EASYJTAG\n"
                "━━━━━━━━━━━━\n"
                "🔹 Model: Vivo V2430\n"
                "🔹 Brand: PD3442f\n"
                "🔹 Android: 15\n"
                "🔹 Security Patch: 2025-08-01\n"
                "🔹 Version: PD2442F_EX_A_15.1.16.0.W20\n"
                "━━━━━━━━━━━━\n"
                "📦 Dump size:\n"
                "Compressed: 5 GB\n"
                "After extraction: 9.5 GB\n"
                "Dump By: EASYJTAG-PLUS\n"
                "━━━━━━━━━━━━\n"
                "🔐 File Password:\n"
                "MobiFirmware.VIP\n"
                "━━━━━━━━━━━━\n"
                "HMAX-UNLOCKER HithamMax"
            )
            btn_download = "📥 Download 5GB - Google Drive"
            btn_back = "⬅️ Back"
        elif lang == "fr":
            txt = (
                "🔥 (2) VIVO Y04 — V2430 — DUMP OSv15 🔥\n"
                "━━━━━━━━━━━━\n"
                "⚙️ Demandé par un membre du groupe\n"
                "👤 ĶĦălěď Ķäbô ❤️\n"
                "━━━━━━━━━━━━\n"
                "📱 VIVO Y04 — V2430\n"
                "⚡ DUMP OSv15 | PAR EASYJTAG\n"
                "━━━━━━━━━━━━\n"
                "🔹 Modèle : Vivo V2430\n"
                "🔹 Marque : PD3442f\n"
                "🔹 Android : 15\n"
                "🔹 Correctif de sécurité : 2025-08-01\n"
                "🔹 Version : PD2442F_EX_A_15.1.16.0.W20\n"
                "━━━━━━━━━━━━\n"
                "📦 Taille du dump :\n"
                "Compressé : 5 GB\n"
                "Après décompression : 9.5 GB\n"
                "Dump par : EASYJTAG-PLUS\n"
                "━━━━━━━━━━━━\n"
                "🔐 Mot de passe du fichier :\n"
                "MobiFirmware.VIP\n"
                "━━━━━━━━━━━━\n"
                "HMAX-UNLOCKER HithamMax"
            )
            btn_download = "📥 Télécharger 5GB - Google Drive"
            btn_back = "⬅️ Retour"
        else:
            txt = (
                "🔥 (2) VIVO Y04 — V2430 — OSv15 DUMP 🔥\n"
                "━━━━━━━━━━━━\n"
                "⚙️ بناءً على طلب عضو الجروب\n"
                "👤 ĶĦălěď Ķäbô ❤️\n"
                "━━━━━━━━━━━━\n"
                "📱 VIVO Y04 — V2430\n"
                "⚡ OSv15 DUMP | BY EASYJTAG\n"
                "━━━━━━━━━━━━\n"
                "🔹 Model: Vivo V2430\n"
                "🔹 Brand: PD3442f\n"
                "🔹 Android: 15\n"
                "🔹 Security Patch: 2025-08-01\n"
                "🔹 Version: PD2442F_EX_A_15.1.16.0.W20\n"
                "━━━━━━━━━━━━\n"
                "📦 حجم الدامب:\n"
                "مضغوط: 5 GB\n"
                "بعد فك الضغط: 9.5 GB\n"
                "Dump By: EASYJTAG-PLUS\n"
                "━━━━━━━━━━━━\n"
                "🔐 File Password:\n"
                "MobiFirmware.VIP\n"
                "━━━━━━━━━━━━\n"
                "HMAX-UNLOCKER HithamMax"
            )
            btn_download = "📥 تحميل 5GB - Google Drive"
            btn_back = "⬅️ رجوع"

        markup.add(types.InlineKeyboardButton(btn_download, url=gdrive_url))
        markup.add(types.InlineKeyboardButton(
            btn_back,
            callback_data="dump_vivo_full_section",
        ))
        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(
                    call.message.chat.id,
                    photo,
                    caption=txt,
                    reply_markup=markup,
                )
        except Exception as e:
            print(f"Send VIVO Y04 (2) photo failed: {e}")
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    # ===== VIVO Y27 & Y36 5G (V2248) PD2279F - Full Dump [RARE] =====
    elif cd == "dump_model_vivo_y27_y36_5g_v2248_pd2279f_ex_a_15_2_10_2_w20":
        markup = types.InlineKeyboardMarkup(row_width=1)
        gdrive_url = "https://drive.google.com/file/d/14Kuvpi_9UtSH_5jkmMmimIkmm6iK8pKZ/view"
        photo_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "images",
            "vivo_y27_y36_5g_v2248_dump_7_3gb_hmax.jpg",
        )

        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass
        try:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except Exception:
            pass

        txt = (
            "🔥 VIVO Y27 & Y36 5G — V2248 — FULL DUMP RARE 🔥\n"
            "━━━━━━━━━━━━\n"
            "📱 DUMP SERIES | VIVO\n"
            "Model: VIVO Y27 & Y36 5G — V2248\n"
            "Firmware: PD2279F_EX_A_15.2.10.2.W20\n"
            "━━━━━━━━━━━━\n"
            "📋 Device Information:\n"
            "• Device: V2248\n"
            "• Name: V2248\n"
            "• Manufacturer: vivo\n"
            "• Brand: vivo\n"
            "• Model: V2248; 1; PD2279F_EX\n"
            "• Platform: MTK6833; mt6833; mt6631_6635; connac1x\n"
            "• Version: PD2279F_EX_A_15.2.10.2.W20\n"
            "• Firmware: Funtouch OS 15; PD2279F_EX_A_15.2.10.2.W20.V000L1\n"
            "• Firmware date: Mon May 19 21:18:38 CST 2025\n"
            "• Incremental: compiler250519211703; 15.2.10.2.W20; compiler250519212336\n"
            "• Android: 15\n"
            "• Security patch: 2025-05-01\n"
            "• ABI: arm64-v8a\n"
            "• Board: k6833v1_64_k510\n"
            "━━━━━━━━━━━━\n"
            "🛠️ TOOLS SUPPORT ✅\n"
            "✅ EASYJTAG-PLUS\n"
            "✅ FLASH64 ULTRA\n"
            "✅ MIPI TESTER\n"
            "━━━━━━━━━━━━\n"
            "💾 Dump Size:\n"
            "• Compressed: 7.3 GB\n"
            "• Extracted: 17 GB\n"
            "🔐 Password: MobiFirmware.VIP\n"
            "☁️ Hosting: Google Drive\n"
            "━━━━━━━━━━━━\n"
            "HMAX-UNLOCKER - HithamMax\n"
        )
        txt = _dump_card_text(user_id, "dump_model_vivo_y27_y36_5g_v2248_pd2279f_ex_a_15_2_10_2_w20", txt)
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📥 Download - Google Drive"), url=gdrive_url))
        markup.add(types.InlineKeyboardButton(_dump_back_label(user_id, "🔙 Back"), callback_data="dump_vivo_full_section"))
        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(
                    call.message.chat.id,
                    photo,
                    caption=txt,
                    reply_markup=markup,
                )
        except Exception as e:
            print(f"Send VIVO Y27 & Y36 dump photo failed: {e}")
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    elif cd == "dump_model_vivo_y21d_pd2510f":
        markup = types.InlineKeyboardMarkup(row_width=1)
        gdrive_url = "https://drive.google.com/file/d/18qzexyLM46cv_rsa9f04tvKZceTJjbJ2/view"
        photo_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "images",
            "vivo_y21d_pd2510f.png",
        )

        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass
        try:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except Exception:
            pass

        txt = (
            "🔥 VIVO Y21D (PD2510F) FULL DUMP 🔥\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "📱 Device: VIVO Y21D\n"
            "🔢 Model: PD2510F\n"
            "💾 Storage: 256GB UFS\n"
            "📂 File: DUMP FILE (RAR)\n"
            "📏 Dump Size: 8.2 GB\n"
            "🛠️ Dumped With: F64 ULTRA\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "👤 Uploaded By: Reynold Bermil Leonido\n"
            "🏷️ Credit: DUMPING-FIRMWARE\n"
            "☁️ Upload Server: Google Drive\n"
            "🔐 Pass: MobiFirmware.VIP"
        )
        txt = _dump_card_text(user_id, "dump_model_vivo_y21d_pd2510f", txt)
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📥 Download - Google Drive"), url=gdrive_url))
        markup.add(types.InlineKeyboardButton(_dump_back_label(user_id, "🔙 Back"), callback_data="dump_vivo_full_section"))
        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(
                    call.message.chat.id,
                    photo,
                    caption=txt,
                    reply_markup=markup,
                )
        except Exception as e:
            print(f"Send VIVO Y21D photo failed: {e}")
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return
    elif cd == "dump_model_vivo_y03t_pd2360f":
        markup = types.InlineKeyboardMarkup(row_width=1)
        gdrive_url = "https://drive.google.com/file/d/1S6oZd5TGZHOfT8Yt6QgeQoYKQ8gAuYJr/view"
        photo_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "images",
            "vivo_y03t_pd2360f.png",
        )

        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass
        try:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except Exception:
            pass

        txt = (
            "🔥 VIVO Y03T (PD2360F) FULL DUMP 🔥\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "📱 Device: VIVO Y03T\n"
            "🔢 Model: PD2360F\n"
            "💾 Storage: 64GB eMMC\n"
            "📂 File: DUMP FILE (RAR)\n"
            "📌 Version: PD2360F_EX_A_14.0.12.3.W20.V000L1\n"
            "📏 Dump Size: 4.9 GB\n"
            "🛠️ Dumped With: F64 ULTRA\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "👤 Uploaded By: Reynold Bermil Leonido\n"
            "🏷️ Credit: DUMPING-FIRMWARE\n"
            "☁️ Upload Server: Google Drive\n"
            "🔐 Pass: MobiFirmware.VIP"
        )
        txt = _dump_card_text(user_id, "dump_model_vivo_y03t_pd2360f", txt)
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📥 Download - Google Drive"), url=gdrive_url))
        markup.add(types.InlineKeyboardButton(_dump_back_label(user_id, "🔙 Back"), callback_data="dump_vivo_full_section"))
        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(
                    call.message.chat.id,
                    photo,
                    caption=txt,
                    reply_markup=markup,
                )
        except Exception as e:
            print(f"Send VIVO Y03T photo failed: {e}")
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return
    elif cd == "dump_model_vivo_y18_pd2327f":
        lang = hmaxi18n.get_language(user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        gdrive_url = "https://drive.google.com/file/d/1a0oOV43ud0t9L149BD1pKRj1MK4LAGGH/view"
        photo_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "images",
            "vivo_y18_pd2327f.png",
        )

        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass
        try:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except Exception:
            pass

        if lang == "en":
            txt = (
                "🔥 VIVO Y18 (PD2327F) FULL DUMP 🔥\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                "📱 Device: VIVO Y18\n"
                "🔢 Model: PD2327F\n"
                "💾 Storage: 128GB eMMC\n"
                "📂 File: DUMP FILE (RAR)\n"
                "📌 Version: PD2327F_EX_A_15.1.17.0.W20.V000L1\n"
                "📏 Dump Size: 4.4 GB\n"
                "🛠️ Dumped With: F64 ULTRA\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                "☁️ Upload Server: Google Drive\n"
                "🔐 Pass: MobiFirmware.VIP"
            )
            btn_download = "📥 Download - Google Drive"
            btn_back = "🔙 Back"
        elif lang == "fr":
            txt = (
                "🔥 DUMP COMPLET VIVO Y18 (PD2327F) 🔥\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                "📱 Appareil : VIVO Y18\n"
                "🔢 Modèle : PD2327F\n"
                "💾 Stockage : 128GB eMMC\n"
                "📂 Fichier : FICHIER DUMP (RAR)\n"
                "📌 Version : PD2327F_EX_A_15.1.17.0.W20.V000L1\n"
                "📏 Taille du DUMP : 4.4 GB\n"
                "🛠️ Extrait avec : F64 ULTRA\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                "☁️ Serveur : Google Drive\n"
                "🔐 Mot de passe : MobiFirmware.VIP"
            )
            btn_download = "📥 Télécharger - Google Drive"
            btn_back = "🔙 Retour"
        else:  # ar هو الافتراضي
            txt = (
                "🔥 دامب كامل VIVO Y18 (PD2327F) 🔥\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                "📱 الجهاز: VIVO Y18\n"
                "🔢 الموديل: PD2327F\n"
                "💾 التخزين: 128GB eMMC\n"
                "📂 الملف: ملف دامب (RAR)\n"
                "📌 الإصدار: PD2327F_EX_A_15.1.17.0.W20.V000L1\n"
                "📏 حجم الدامب: 4.4 GB\n"
                "🛠️ تم السحب بواسطة: F64 ULTRA\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                "☁️ سيرفر الرفع: Google Drive\n"
                "🔐 كلمة المرور: MobiFirmware.VIP"
            )
            btn_download = "📥 تحميل - Google Drive"
            btn_back = "🔙 رجوع"
        markup.add(types.InlineKeyboardButton(btn_download, url=gdrive_url))
        markup.add(types.InlineKeyboardButton(btn_back, callback_data="dump_vivo_full_section"))
        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(
                    call.message.chat.id,
                    photo,
                    caption=txt,
                    reply_markup=markup,
                )
        except Exception as e:
            print(f"Send VIVO Y18 photo failed: {e}")
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    elif cd == "dump_model_vivo_y22s_pd2228f":
        lang = hmaxi18n.get_language(user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        gdrive_url = "https://drive.google.com/file/d/1myQP49q9I-RuOFciiCwt93pVjC50bLCC/view"
        photo_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "images",
            "vivo_y22s_pd2228f.png",
        )

        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass
        try:
            bot.delete_message(chat_id=user_id, message_id=call.message.message_id)
        except Exception:
            pass

        # Drive displays the archive size as 4.5G; keep it approximate.
        if lang == "en":
            txt = (
                "📋 FIRMWARE SPEC CARD\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                "📱 Device: VIVO Y22S\n"
                "🔢 Model: PD2228F\n"
                "💾 Storage: 128GB UFS\n"
                "📌 Firmware: PD2228F_EX_A_14.2.8.0.W20.V000L1\n"
                "📂 File: DUMP (RAR)\n"
                "📏 Archive size: ≈4.5 GB\n"
                "🛠️ Dumped with: F64 BOX\n"
                "☁️ Server: Google Drive"
            )
            btn_download = "📥 Download - Google Drive"
            btn_back = "🔙 Back"
        elif lang == "fr":
            txt = (
                "📋 FICHE TECHNIQUE DU FIRMWARE\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                "📱 Appareil : VIVO Y22S\n"
                "🔢 Modèle : PD2228F\n"
                "💾 Stockage : 128GB UFS\n"
                "📌 Firmware : PD2228F_EX_A_14.2.8.0.W20.V000L1\n"
                "📂 Fichier : DUMP (RAR)\n"
                "📏 Taille de l’archive : ≈4.5 GB\n"
                "🛠️ Extrait avec : F64 BOX\n"
                "☁️ Serveur : Google Drive"
            )
            btn_download = "📥 Télécharger - Google Drive"
            btn_back = "🔙 Retour"
        else:  # Arabic is the default language.
            txt = (
                "📋 بطاقة مواصفات الفيرموير\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                "📱 الجهاز: VIVO Y22S\n"
                "🔢 الموديل: PD2228F\n"
                "💾 التخزين: 128GB UFS\n"
                "📌 الفيرموير: PD2228F_EX_A_14.2.8.0.W20.V000L1\n"
                "📂 الملف: دامب (RAR)\n"
                "📏 حجم الأرشيف: ≈4.5 GB\n"
                "🛠️ تم السحب بواسطة: F64 BOX\n"
                "☁️ السيرفر: Google Drive"
            )
            btn_download = "📥 تحميل - Google Drive"
            btn_back = "🔙 رجوع"

        markup.add(types.InlineKeyboardButton(btn_download, url=gdrive_url))
        markup.add(types.InlineKeyboardButton(btn_back, callback_data="dump_vivo_full_section"))
        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(user_id, photo, caption=txt, reply_markup=markup)
        except Exception as e:
            print(f"Send VIVO Y22S photo failed: {e}")
            bot.send_message(user_id, txt, reply_markup=markup)
        return

    # ===== 📦 VIVO Y15s (V2120) PD2140F - 2 Versions Full Dump [UnlockTool] =====
    elif cd == "dump_model_vivo_y15s_v2120_pd2140f_full_dump_unlocktool":
        markup = types.InlineKeyboardMarkup(row_width=1)
        old_url = "https://drive.google.com/file/d/1ZzXLLhmGSoU5FkNqEvkSMTEZ2dPhHUrc/view"
        new_url = "https://drive.google.com/file/d/1CCH-oDVN-Erjh1O0o3sEZcnH4QWQX-Mc/view"
        photo_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "images",
            "vivo_y15s_v2120_pd2140f_2_versions_full_dump_unlocktool.jpg",
        )
        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass
        try:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except Exception:
            pass
        txt = (
            "🔥 Vivo Y15s (V2120) – PD2140F | Full Dump BY UnlockTool 🔥\n"
            "━━━━━━━━━━━━\n"
            "📱 من فترة كبيرة كنا رفعنا Dump لنفس الهاتف:\n"
            "🖤 Vivo Y15s (V2120)\n"
            "🔧 Model: PD2140F\n"
            "📦 Version: PD2140F_EX_A_6.37.2\n"
            "🔧 Dump By: UnlockTool\n"
            "🔗 رابط الدامب السابق\n"
            "🔐 Pass File: MobiFirmware.VIP\n"
            "━━━━━━━━━━━━\n"
            "💥 النهارده بنضيف Dump جديد لنفس الهاتف بإصدار مختلف:\n"
            "🖤 Vivo Y15s (V2120)\n"
            "🔧 Model: PD2140F\n"
            "📦 Version: PD2140F_EX_A_6.45.5 NEW\n"
            "🔧 Dump By: UnlockTool\n"
            "🔐 Pass File: MobiFirmware.VIP\n"
            "━━━━━━━━━━━━━\n"
            "❓ ليه دامب تاني لنفس الهاتف؟ ملاحظه مهمه\n"
            "ناس كتير ممكن تشتغل بالدامب اللي كان موجود بالفعل في الجروب،\n"
            "لكن حبينا نوفر الإصدار ده كمان ونخليه متاح معانا،\n"
            "لأن اختلاف إصدارات السوفتوير أحيانًا بيكون سبب مهم في نجاح عملية الإصلاح.\n"
            "والدامبين زي ما وضحنا فوق مسحوبين بواسطة UnlockTool.\n"
            "━━━━━━━━━━━━\n"
            "⚠️ مهم جدًا قبل التفليش:\n"
            "يرجى سحب وحفظ ملفات الشبكة (Network Files) قبل البدء في عملية التفليش.\n"
            "━━━━━━━━━━━━\n"
            "HMAX-UNLOCKER HithamMax\n"
        )
        txt = _dump_card_text(user_id, "dump_model_vivo_y15s_v2120_pd2140f_full_dump_unlocktool", txt)
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📥 V6.37.2 OLD Download"), url=old_url))
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📥 V6.45.5 NEW Download"), url=new_url))
        markup.add(types.InlineKeyboardButton(_dump_back_label(user_id, "⬅️ Back"), callback_data="dump_vivo_full_section"))
        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(call.message.chat.id, photo, caption=txt, reply_markup=markup)
        except Exception as e:
            print(f"Photo error: {e}")
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    elif cd == "dump_other_full_section":
        lang = hmaxi18n.get_language(user_id)
        t = {
            "ar": {
                "title": "💿 OTHER DUMP - اختر الموديل",
                "ravoz": "📱 RAVOZ V7 - Full Dump [3.5GB] - FREE",
                "poco": "📱 POCO C65 - 256GB [F64 ULTRA]",
                "lenovo": "📱 LENOVO TB-7305X - Scatter",
                "blu": "📱 BLU T5 TIGO - T0050TT V9.0.G.06.04 [CM2] NEW",
                "lava": "📱 LAVA Iris 59 LE9930 S121 EGY [PANDORA] NEW",
                "walton": "📱 WALTON NEXG N72 Full Dump + Nv [PANDORA] NEW",
                "back": "⬅️ رجوع لـ DUMP",
            },
            "en": {
                "title": "💿 OTHER DUMP - Select Model",
                "ravoz": "📱 RAVOZ V7 - Full Dump [3.5GB] - FREE",
                "poco": "📱 POCO C65 - 256GB [F64 ULTRA]",
                "lenovo": "📱 LENOVO TB-7305X - Scatter",
                "blu": "📱 BLU T5 TIGO - T0050TT [CM2] NEW",
                "lava": "📱 LAVA Iris 59 LE9930 [PANDORA] NEW",
                "walton": "📱 WALTON NEXG N72 [PANDORA] NEW",
                "back": "⬅️ Back to DUMP",
            },
            "fr": {
                "title": "💿 OTHER DUMP - Sélectionner modèle",
                "ravoz": "📱 RAVOZ V7 - Dump Complet [3,5GB] - GRATUIT",
                "poco": "📱 POCO C65 - 256GB [F64 ULTRA]",
                "lenovo": "📱 LENOVO TB-7305X - Scatter",
                "blu": "📱 BLU T5 TIGO - T0050TT [CM2] NOUVEAU",
                "lava": "📱 LAVA Iris 59 [PANDORA] NOUVEAU",
                "walton": "📱 WALTON NEXG N72 [PANDORA] NOUVEAU",
                "back": "⬅️ Retour à DUMP",
            },
        }
        l = t.get(lang, t["ar"])
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton(l["ravoz"], callback_data="dump_model_ravoz_v7"))
        # باقي الموديلات اللي عندك
        markup.add(types.InlineKeyboardButton(l["poco"], callback_data="dump_model_poco_c65_256gb"))
        markup.add(types.InlineKeyboardButton(l["lenovo"], callback_data="dump_lenovo_tb_7305x"))
        markup.add(types.InlineKeyboardButton(l["blu"], callback_data="dump_model_blu_t5_tigo"))
        markup.add(types.InlineKeyboardButton(l["lava"], callback_data="dump_model_lava_iris_59"))
        markup.add(types.InlineKeyboardButton(l["walton"], callback_data="dump_model_walton_nexg_n72"))
        markup.add(types.InlineKeyboardButton(l["back"], callback_data="dump_main_section"))
        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass
        _hmax_show_menu(call, l["title"], markup)
        return

    elif cd == "dump_model_ravoz_v7":
        lang = hmaxi18n.get_language(user_id)
        gdrive_url = "https://drive.google.com/file/d/1qcGLeJIGgmwKVTHa-sdvUyuIYeZAv5dc/view"
        photo_path = "images/ravoz_v7_hmax.jpg"
        try:
            bot.answer_callback_query(call.id)
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except Exception:
            pass

        txts = {
            "ar": (
                "🔥 دامب RAVOZ V7 متاح مجانًا 🔥\n"
                "━━━━━━━━━━━━\n"
                "📱 RAVOZ V7 — Full Backup Dump\n"
                "🔨 تم سحب الدامب بواسطة PandoraTool\n"
                "📱 Android 14\n"
                "💾 حجم الدامب: 3.5 جيجا\n"
                "☁️ مرفوع على Google Drive\n"
                "✅ تم الاختبار بنجاح 100%\n"
                "━━━━━━━━━━━━\n"
                "📦 Model: RAVOZ V7\n"
                "📁 File: Full Dump\n"
                "🔨 Tool: PandoraTool\n"
                "🛠️ Android Version: 14\n"
                "🆔 Build ID: TP1A.220624.014\n"
                "💾 Total Size: 3.58 GB\n"
                "━━━━━━━━━━━━\n"
                "🔑 كلمة مرور الملف: MobiFirmware.VIP\n"
                "━━━━━━━━━━━━\n"
                "HMAX-UNLOCKER - HithamMax\n"
                "🔐 MobiFirmware.VIP"
            ),
            "en": (
                "🔥 RAVOZ V7 Dump Available FREE 🔥\n"
                "━━━━━━━━━━━━\n"
                "📱 RAVOZ V7 — Full Backup Dump\n"
                "🔨 Dumped by PandoraTool\n"
                "📱 Android 14\n"
                "💾 Size: 3.5 GB\n"
                "☁️ Uploaded to Google Drive\n"
                "✅ Tested 100% Successfully\n"
                "━━━━━━━━━━━━\n"
                "📦 Model: RAVOZ V7\n"
                "📁 File: Full Dump\n"
                "🔨 Tool: PandoraTool\n"
                "🛠️ Android Version: 14\n"
                "🆔 Build ID: TP1A.220624.014\n"
                "💾 Total Size: 3.58 GB\n"
                "━━━━━━━━━━━━\n"
                "🔑 Password: MobiFirmware.VIP\n"
                "━━━━━━━━━━━━\n"
                "HMAX-UNLOCKER - HithamMax\n"
                "🔐 MobiFirmware.VIP"
            ),
            "fr": (
                "🔥 Dump RAVOZ V7 disponible GRATUIT 🔥\n"
                "━━━━━━━━━━━━\n"
                "📱 RAVOZ V7 — Full Backup Dump\n"
                "🔨 Extrait avec PandoraTool\n"
                "📱 Android 14\n"
                "💾 Taille: 3,5 Go\n"
                "☁️ Hébergé sur Google Drive\n"
                "✅ Testé 100% avec succès\n"
                "━━━━━━━━━━━━\n"
                "📦 Model: RAVOZ V7\n"
                "📁 Fichier: Full Dump\n"
                "🔨 Outil: PandoraTool\n"
                "🛠️ Version Android: 14\n"
                "🆔 Build ID: TP1A.220624.014\n"
                "💾 Taille totale: 3,58 Go\n"
                "━━━━━━━━━━━━\n"
                "🔑 Mot de passe: MobiFirmware.VIP\n"
                "━━━━━━━━━━━━\n"
                "HMAX-UNLOCKER - HithamMax\n"
                "🔐 MobiFirmware.VIP"
            ),
        }
        txt = txts.get(lang, txts["ar"])
        btn_dl = {
            "ar": "📥 رابط تحميل الدامب - 3.5GB",
            "en": "📥 Download Dump - 3.5GB",
            "fr": "📥 Lien Dump - 3,5Go",
        }.get(lang, "📥 Download")
        btn_back = {
            "ar": "⬅️ رجوع لـ OTHER",
            "en": "⬅️ Back to OTHER",
            "fr": "⬅️ Retour à OTHER",
        }.get(lang, "⬅️ Back")

        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton(btn_dl, url=gdrive_url))
        markup.add(types.InlineKeyboardButton(btn_back, callback_data="dump_other_full_section"))
        try:
            with open(photo_path, 'rb') as photo:
                bot.send_photo(call.message.chat.id, photo, caption=txt, reply_markup=markup)
        except Exception:
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    elif cd == "dump_model_poco_c65_256gb":
        lang = hmaxi18n.get_language(user_id)
        translations = {
            "ar": {
                "details": (
                    "🔥 دامب كامل XIAOMI POCO C65 - 256GB\n"
                    "🔖 إصدار الدامب: MAY.1 2025\n"
                    "🛠️ تم السحب بواسطة: F64 ULTRA\n"
                    "📏 الحجم: 7GB\n"
                    "🔑 كلمة المرور: MobiFirmware.VIP"
                ),
                "download": "📥 رابط Google Drive",
                "back": "🔙 رجوع إلى دامبات أخرى",
                "footer": (
                    "⚠️ حقوق HMAX - هيثم ماكس\n"
                    "📱 واتساب: https://wa.me/message/A3KQWHSSERCFG1\n"
                    "📘 فيسبوك: https://www.facebook.com/share/1C3JnWP5bM/\n"
                    "✈️ تيليجرام: @hithammax"
                ),
            },
            "en": {
                "details": (
                    "🔥 XIAOMI POCO C65 - 256GB FULL DUMP\n"
                    "🔖 Dump Version: MAY.1 2025\n"
                    "🛠️ Dumped With: F64 ULTRA\n"
                    "📏 Size: 7GB\n"
                    "🔑 PASS: MobiFirmware.VIP"
                ),
                "download": "📥 Google Drive Link",
                "back": "🔙 Back to Other DUMPs",
                "footer": (
                    "⚠️ HMAX - Haitham Max Copyright Notice\n"
                    "📱 WhatsApp: https://wa.me/message/A3KQWHSSERCFG1\n"
                    "📘 Facebook: https://www.facebook.com/share/1C3JnWP5bM/\n"
                    "✈️ Telegram: @hithammax"
                ),
            },
            "fr": {
                "details": (
                    "🔥 DUMP COMPLET XIAOMI POCO C65 - 256GB\n"
                    "🔖 Version du dump : MAY.1 2025\n"
                    "🛠️ Extrait avec : F64 ULTRA\n"
                    "📏 Taille : 7GB\n"
                    "🔑 MOT DE PASSE : MobiFirmware.VIP"
                ),
                "download": "📥 Lien Google Drive",
                "back": "🔙 Retour aux autres DUMP",
                "footer": (
                    "⚠️ Droits d'auteur HMAX - Haitham Max\n"
                    "📱 WhatsApp : https://wa.me/message/A3KQWHSSERCFG1\n"
                    "📘 Facebook : https://www.facebook.com/share/1C3JnWP5bM/\n"
                    "✈️ Telegram : @hithammax"
                ),
            },
        }
        labels = translations.get(lang, translations["ar"])
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton(
            labels["download"],
            url="https://drive.google.com/file/d/1nT9Eb1NtNSxodYzYSPBqVcynvQqNwbdO/view",
        ))
        markup.add(types.InlineKeyboardButton(
            labels["back"],
            callback_data="dump_other_full_section",
        ))
        bot.edit_message_text(
            f'{labels["details"]}\n\n{labels["footer"]}',
            user_id,
            call.message.message_id,
            reply_markup=markup,
        )
        return

    elif cd == "dump_lenovo_tb_7305x":
        lang = hmaxi18n.get_language(user_id)
        gdrive_url = "https://drive.google.com/file/d/1B5VzL2H1A51NQ33_H6C8vDywObFolbz7/view"
        photo_path = "images/lenovo_tb_7305x_scatter_hmax.jpg"
        try:
            bot.answer_callback_query(call.id)
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except Exception:
            pass

        txts = {
            "ar": (
                "🔥 Lenovo TB-7305X - Scatter 🔥\n"
                "━━━━━━━━━━━━\n"
                "📱 Model: TB-7305X\n"
                "📁 File: Scatter Firmware\n"
                "🔨 Tool: SP Flash Tool\n"
                "🔑 Pass File: MobiFirmware.VIP\n"
                "☁️ مرفوع على Google Drive\n"
                "✅ تم الاختبار 100%\n"
                "━━━━━━━━━━━━\n"
                "HMAX-UNLOCKER - HithamMax"
            ),
            "en": (
                "🔥 Lenovo TB-7305X - Scatter 🔥\n"
                "📱 Model: TB-7305X\n"
                "📁 File: Scatter\n"
                "🔨 Tool: SP Flash Tool\n"
                "🔑 Password: MobiFirmware.VIP\n"
                "☁️ Google Drive\n"
                "✅ Tested 100%\n"
                "HMAX-UNLOCKER"
            ),
            "fr": (
                "🔥 Lenovo TB-7305X - Scatter 🔥\n"
                "📱 Model: TB-7305X\n"
                "📁 Fichier: Scatter\n"
                "🔨 Outil: SP Flash Tool\n"
                "🔑 Mot de passe: MobiFirmware.VIP\n"
                "☁️ Google Drive\n"
                "✅ Testé 100%\n"
                "HMAX-UNLOCKER"
            ),
        }
        txt = txts.get(lang, txts["ar"])
        btn_dl = {
            "ar": "📥 تحميل Scatter - TB-7305X",
            "en": "📥 Download Scatter - TB-7305X",
            "fr": "📥 Télécharger Scatter",
        }.get(lang, "📥 Download Scatter - TB-7305X")
        btn_back = {
            "ar": "⬅️ رجوع لـ OTHER",
            "en": "⬅️ Back to OTHER",
            "fr": "⬅️ Retour à OTHER",
        }.get(lang, "⬅️ Back to OTHER")

        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton(btn_dl, url=gdrive_url))
        markup.add(types.InlineKeyboardButton(btn_back, callback_data="dump_other_full_section"))
        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(call.message.chat.id, photo, caption=txt, reply_markup=markup)
        except Exception:
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    elif cd == "dump_model_blu_t5_tigo":
        lang = hmaxi18n.get_language(user_id)
        terabox_url = "https://www.terabox.app/arabic/sharing/link?surl=TLasYwRnDISWcAK9WLzB3Q"
        photo_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "images",
            "blu_t5_tigo_t0050tt_hmax_real.jpg",
        )
        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass
        try:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except Exception:
            pass

        txts = {
            "ar": (
                "🔥 BLU T5 TIGO - T0050TT 🔥\n"
                "━━━━━━━━━━━━\n"
                "📱 Model: T0050TT\n"
                "🔖 V9.0.G.06.04_TIGO_30-12-2020_1638\n"
                "🛠️ Dump BY CM2\n"
                "🔑 Pass: MobiFirmware.VIP\n"
                "☁️ Terabox\n"
                "━━━━━━━━━━━━\n"
                "⚠️ ملاحظه مهمه لازم تفتح VPN سايفون على شان يظهر لك رابط التحميل\n"
                "━━━━━━━━━━━━\n"
                "HMAX-UNLOCKER - HithamMax"
            ),
            "en": (
                "🔥 BLU T5 TIGO - T0050TT 🔥\n"
                "📱 Model: T0050TT\n"
                "🔖 V9.0.G.06.04_TIGO_30-12-2020_1638\n"
                "🛠️ Dump BY CM2\n"
                "🔑 Password: MobiFirmware.VIP\n"
                "☁️ Server: Terabox\n"
                "⚠️ Important: Open Psiphon VPN so the download link shows up\n"
                "HMAX-UNLOCKER"
            ),
            "fr": (
                "🔥 BLU T5 TIGO - T0050TT 🔥\n"
                "📱 Modèle: T0050TT\n"
                "🔖 V9.0.G.06.04_TIGO_30-12-2020_1638\n"
                "🛠️ Dump par CM2\n"
                "🔑 Mot de passe: MobiFirmware.VIP\n"
                "☁️ Serveur: Terabox\n"
                "⚠️ Important: Ouvrez VPN Psiphon pour voir le lien de téléchargement\n"
                "HMAX-UNLOCKER"
            ),
        }
        txt = txts.get(lang, txts["ar"])
        btn_dl = {
            "ar": "📥 تحميل من Terabox - VPN سايفون مطلوب",
            "en": "📥 Download Terabox - Need VPN",
            "fr": "📥 Télécharger Terabox - VPN requis",
        }.get(lang, "📥 تحميل من Terabox - VPN سايفون مطلوب")
        btn_back = {
            "ar": "⬅️ رجوع لـ OTHER",
            "en": "⬅️ Back to OTHER",
            "fr": "⬅️ Retour à OTHER",
        }.get(lang, "⬅️ رجوع لـ OTHER")

        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton(btn_dl, url=terabox_url))
        markup.add(types.InlineKeyboardButton(btn_back, callback_data="dump_other_full_section"))
        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(call.message.chat.id, photo, caption=txt, reply_markup=markup)
        except Exception:
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    elif cd == "dump_model_lava_iris_59":
        lang = hmaxi18n.get_language(user_id)
        terabox_url = "https://www.terabox.app/arabic/sharing/link?surl=-okpAZRO3RAKy-8YIrP7sQ"
        photo_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "images",
            "lava_iris_59_le9930_hmax.jpg",
        )
        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass
        try:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except Exception:
            pass

        txts = {
            "ar": (
                "🔥 LAVA Iris 59 - LE9930 🔥\n"
                "━━━━━━━━━━━━\n"
                "📱 S121_EGY_21G22_ALL_VERSIONS\n"
                "🛠️ DUMP BY Pandora Tool\n"
                "🔑 Pass: MobiFirmware.VIP\n"
                "☁️ Terabox\n"
                "━━━━━━━━━━━━\n"
                "⚠️ افتح VPN سايفون على شان يظهر لك رابط التحميل\n"
                "━━━━━━━━━━━━\n"
                "HMAX-UNLOCKER - HithamMax"
            ),
            "en": (
                "🔥 LAVA Iris 59 - LE9930 🔥\n"
                "📱 Version: S121_EGY_21G22_ALL_VERSIONS\n"
                "🛠️ DUMP BY Pandora Tool\n"
                "🔑 Password: MobiFirmware.VIP\n"
                "☁️ Server: Terabox\n"
                "⚠️ Important: Open Psiphon VPN so the download link shows up\n"
                "HMAX-UNLOCKER"
            ),
            "fr": (
                "🔥 LAVA Iris 59 - LE9930 🔥\n"
                "📱 Version: S121_EGY_21G22_ALL_VERSIONS\n"
                "🛠️ DUMP par Pandora Tool\n"
                "🔑 Mot de passe: MobiFirmware.VIP\n"
                "☁️ Serveur: Terabox\n"
                "⚠️ Important: Ouvrez VPN Psiphon pour voir le lien de téléchargement\n"
                "HMAX-UNLOCKER"
            ),
        }
        txt = txts.get(lang, txts["ar"])
        btn_dl = {
            "ar": "📥 تحميل من Terabox - VPN سايفون مطلوب",
            "en": "📥 Download Terabox - Need VPN",
            "fr": "📥 Télécharger Terabox - VPN requis",
        }.get(lang, "📥 تحميل من Terabox - VPN سايفون مطلوب")
        btn_back = {
            "ar": "⬅️ رجوع لـ OTHER",
            "en": "⬅️ Back to OTHER",
            "fr": "⬅️ Retour à OTHER",
        }.get(lang, "⬅️ رجوع لـ OTHER")

        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton(btn_dl, url=terabox_url))
        markup.add(types.InlineKeyboardButton(btn_back, callback_data="dump_other_full_section"))
        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(call.message.chat.id, photo, caption=txt, reply_markup=markup)
        except Exception:
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    elif cd == "dump_model_walton_nexg_n72":
        lang = hmaxi18n.get_language(user_id)
        terabox_url = "https://www.terabox.app/arabic/sharing/link?surl=UfydmqOdzA2ciqvCRFF_9A"
        photo_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "images",
            "walton_nexg_n72_hmax.jpg",
        )
        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass
        try:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except Exception:
            pass

        txts = {
            "ar": (
                "🔥 WALTON NEXG N72 🔥\n"
                "━━━━━━━━━━━━\n"
                "📂 Full Dump And Nv\n"
                "🛠️ DUMP BY Pandora Tool\n"
                "🔑 Pass: MobiFirmware.VIP\n"
                "☁️ Terabox\n"
                "━━━━━━━━━━━━\n"
                "⚠️ افتح VPN سايفون على شان يظهر لك رابط التحميل\n"
                "━━━━━━━━━━━━\n"
                "HMAX-UNLOCKER - HithamMax"
            ),
            "en": (
                "🔥 WALTON NEXG N72 🔥\n"
                "📂 Full Dump And Nv\n"
                "🛠️ DUMP BY Pandora Tool\n"
                "🔑 Password: MobiFirmware.VIP\n"
                "☁️ Server: Terabox\n"
                "⚠️ Important: Open Psiphon VPN so the download link shows up\n"
                "HMAX-UNLOCKER"
            ),
            "fr": (
                "🔥 WALTON NEXG N72 🔥\n"
                "📂 Full Dump And Nv\n"
                "🛠️ DUMP par Pandora Tool\n"
                "🔑 Mot de passe: MobiFirmware.VIP\n"
                "☁️ Serveur: Terabox\n"
                "⚠️ Important: Ouvrez VPN Psiphon pour voir le lien de téléchargement\n"
                "HMAX-UNLOCKER"
            ),
        }
        txt = txts.get(lang, txts["ar"])
        btn_dl = {
            "ar": "📥 تحميل من Terabox - VPN سايفون مطلوب",
            "en": "📥 Download Terabox - Need VPN",
            "fr": "📥 Télécharger Terabox - VPN requis",
        }.get(lang, "📥 تحميل من Terabox - VPN سايفون مطلوب")
        btn_back = {
            "ar": "⬅️ رجوع لـ OTHER",
            "en": "⬅️ Back to OTHER",
            "fr": "⬅️ Retour à OTHER",
        }.get(lang, "⬅️ رجوع لـ OTHER")

        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton(btn_dl, url=terabox_url))
        markup.add(types.InlineKeyboardButton(btn_back, callback_data="dump_other_full_section"))
        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(call.message.chat.id, photo, caption=txt, reply_markup=markup)
        except Exception:
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    elif cd == "dump_iphone_copy_section":
        lang = hmaxi18n.get_language(user_id)
        if lang == "en":
            text = "🍎 iPhone Copy - Official Dump Library\n\nSelect model:"
            back_label = "🔙 Back"
        elif lang == "fr":
            text = "🍎 iPhone Copy - Bibliothèque de dumps\n\nSélectionner le modèle :"
            back_label = "🔙 Retour"
        else:
            text = "🍎 قسم دامبات iPhone Copy\n\nاختر الموديل:"
            back_label = "🔙 رجوع"
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton(
            _dump_btn(user_id, "🔥 iPhone 16 Pro Max Copy MT6735"),
            callback_data="dump_model_iphone16_pro_max_copy_mt6735",
        ))
        markup.add(types.InlineKeyboardButton(
            back_label,
            callback_data="dump_main_section",
        ))
        try:
            bot.answer_callback_query(call.id)
        except Exception as e:
            print(f"Answer iPhone Copy section callback failed: {e}")
        _hmax_show_menu(call, text, markup)
        return

    elif cd in (
        "dump_copy_full_section",
        "dump_copy_section",
    ):
        lang = hmaxi18n.get_language(user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        if lang == "en":
            txt = "💾 *COPY FULL DUMP*\n\nSelect model:"
        else:
            txt = _dump_localize(user_id, "💾 *فل دامب كوبي*\n\nاختر الموديل:")
        markup.add(types.InlineKeyboardButton(
            "📱 SAMSUNG S26 ULTRA COPY - SAMBA65S [PANDORA]",
            callback_data="dump_model_s26_ultra_copy_samba65s",
        ))
        markup.add(types.InlineKeyboardButton(
            "📱 " + "iPh" + "one 17 Pro Copy - DCODE DS-BD2 [ATFELY]",
            callback_data="dump_model_iphone_17_pro_copy_ds_bd2",
        ))
        markup.add(types.InlineKeyboardButton(
            "⚠️ S26 Ultra COPY MT6580 - CM2 - FAKE DETECTED",
            callback_data="dump_model_copy_s26_ultra_mt6580",
        ))
        markup.add(types.InlineKeyboardButton(
            "🔥 REALME C67 COPY - FULL DUMP 1.1GB [Pandora]",
            callback_data="dump_model_realme_c67_copy_full_dump_pandora",
        ))
        markup.add(types.InlineKeyboardButton(
            "🔙 رجوع" if lang != "en" else "🔙 Back",
            # COPY lives inside the DUMP brand menu, so back returns there.
            callback_data="dump_main_section",
        ))
        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass
        _hmax_show_menu(call, txt, markup, parse_mode="Markdown")
        return

    elif cd == "dump_model_copy_s26_ultra_mt6580":
        markup = types.InlineKeyboardMarkup(row_width=1)
        gdrive_url = "https://drive.google.com/file/d/1imGiG3ca2omwJBxJQWsYl2w0SAObQAhl/view"
        photo_path = "images/copy_s26_ultra_mt6580_cm2.jpg"
        try:
            bot.answer_callback_query(call.id)
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except:
            pass
        txt = (
            "⚠️ دامب جديد لأجهزة الـ COPY | وجب التنبيه ⚠️\n"
            "━━━━━━━━━━━━\n"
            "الجهاز داخل على إنه S25 Ultra\n"
            "الجهاز نفسه قال: استنى يا باشا... أنا S26 Ultra!\n"
            "الخلاصة: الجهاز بالكرتونة حاجة والفلاشة حاجة تانية!\n"
            "━━━━━━━━━━━━\n"
            "📊 DUMP INFORMATION\n"
            "Product Model: S26 Ultra\n"
            "Brand: alps\n"
            "Product Name: S26_Ultra\n"
            "Product Device: S26_Ultra\n"
            "CPU: MT6580\n"
            "Board: k80hd_bsp_fwv_512m\n"
            "Platform: MT6580\n"
            "Android: 8.1.0\n"
            "Patch Level: O11019\n"
            "Security Patch: 2021-03-05\n"
            "Display ID: V207-Q16-MC-Q26-20260114\n"
            "SW Version: 1768383878\n"
            "Build Time: 14/01/2026 09:44:30 AM\n"
            "Architecture: armeabi-v7a / armeabi\n"
            "Dump: FULL DUMP\n"
            "Tool: CM2\n"
            "━━━━━━━━━━━━\n"
            "🔐 Pass: MobiFirmware.VIP\n"
        )
        txt = _dump_card_text(user_id, "dump_model_copy_s26_ultra_mt6580", txt)
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📥 Download - Google Drive"), url=gdrive_url))
        markup.add(types.InlineKeyboardButton(_dump_back_label(user_id, "⬅️ Back"), callback_data="dump_copy_full_section"))
        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(call.message.chat.id, photo, caption=txt, reply_markup=markup)
        except:
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    elif cd == "dump_model_s26_ultra_copy_samba65s":
        lang = hmaxi18n.get_language(user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        gdrive_url = "https://drive.google.com/file/d/1alw0UC9SxIJW9IsHQnXOP9Uvl8xYEAjU/view"

        try:
            bot.answer_callback_query(call.id)
        except:
            pass

        try:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except:
            pass

        # 1. أرسل الفيديو أولاً فوق
        try:
            bot.copy_message(chat_id=call.message.chat.id, from_chat_id="@HMAX_FILE", message_id=6)
        except Exception as e:
            print(f"Copy video failed: {e}")

        # 2. أرسل النص تحت الفيديو - بدون Markdown لتجنب الأخطاء
        if lang == "en":
            txt = (
                "🔥 SAMSUNG S26 ULTRA COPY - FULL DUMP | PANDORA TOOL 🔥\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n"
                "DEVICE INFORMATION\n"
                "Brand: IPRO\n"
                "Model: SAMBA65S\n"
                "Board: sp7731e_1h10\n"
                "Platform: sp7731e\n"
                "Firmware: 41338\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n"
                "SOFTWARE: Android 11 - SDK 30\n"
                "Build: RP1A.201005.001 - 26 March 2026\n"
                "Security Patch: 05 Oct 2021\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n"
                "PASS: MobiFirmware.VIP\n"
                "Source: PANDORA TOOL\n"
                "Contact: wa.me/message/A3KQWHSSERCFG1"
            )
            btn_dl = "📥 Download - Google Drive"
            btn_back = "🔙 Back"
        else:
            txt = (
                "🔥 سامسونج S26 ألترا كوبي - فل دامب | باندورا 🔥\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n"
                "معلومات الجهاز:\n"
                "العلامة: IPRO\n"
                "الموديل: SAMBA65S\n"
                "البورد: sp7731e_1h10\n"
                "المنصة: sp7731e\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n"
                "نظام: Android 11 - SDK 30\n"
                "Build: 26 March 2026\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n"
                "كلمة السر: MobiFirmware.VIP\n"
                "المصدر: PANDORA TOOL\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n"
                "للتواصل: wa.me/message/A3KQWHSSERCFG1\n"
                "فيسبوك: facebook.com/share/1C3JnWP5bM\n"
                "تيليجرام: @hithammax"
            )
            btn_dl = "📥 رابط التحميل - Google Drive"
            btn_back = "🔙 رجوع لقسم الكوبي"

        markup.add(types.InlineKeyboardButton(btn_dl, url=gdrive_url))
        markup.add(types.InlineKeyboardButton(btn_back, callback_data="dump_copy_full_section"))
        # مهم: بدون parse_mode عشان النص ما يفشل
        try:
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        except Exception as e:
            print(f"Send text failed: {e}")
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    elif cd == "dump_model_realme_c67_copy_full_dump_pandora":
        markup = types.InlineKeyboardMarkup(row_width=1)
        gdrive_url = "https://drive.google.com/file/d/1ZFf5jTLPsXjOXU48yb5C_rwmLTiX8BOx/view"
        photo_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "images",
            "realme_c67_copy_full_dump_pandora_prince_cazanova.jpg",
        )
        try:
            bot.answer_callback_query(call.id)
        except Exception as e:
            print(f"Answer REALME C67 COPY callback failed: {e}")
        try:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except Exception as e:
            print(f"Delete COPY menu failed: {e}")
        txt = (
            "🔥 REALME C67 COPY — FULL DUMP 🔥\n"
            "━━━━━━━━━━━━\n"
            "🛠️ FULL DUMP | Pandora Tool\n"
            "👤 By Prince Cazanova\n"
            "📦 File Size: 1.1 GB\n"
            "☁️ Uploaded on Google Drive\n"
            "🔐 Password: MobiFirmware.VIP\n"
            "━━━━━━━━━━━━\n"
            "📋 Dump Information\n"
            "Model: C67\n"
            "Device: C67\n"
            "Board: k80hd_bsp_fwv_512m\n"
            "Platform: MTK6580_8.1\n"
            "Android Version: 8.1.0\n"
            "Build ID: O11019\n"
            "Display ID: O11019 test-keys\n"
            "Security Patch: 2024-03-11\n"
            "Userdata: F2FS\n"
            "━━━━━━━━━━━━\n"
            "⚠️ مهم للفنيين: ملاحظه قبل أي عملية تفليش، يُفضل أخذ Backup كامل لملفات الشبكة والبيانات المهمة والتأكد من مطابقة الإصدار والبورد مع الجهاز لتجنب أي مشاكل.\n"
            "━━━━━━━━━━━━\n"
            "HMAX hithamMax\n"
        )
        txt = _dump_card_text(user_id, "dump_model_realme_c67_copy_full_dump_pandora", txt)
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📥 Download - Google Drive 1.1GB"), url=gdrive_url))
        markup.add(types.InlineKeyboardButton(_dump_back_label(user_id, "⬅️ Back"), callback_data="dump_copy_section"))
        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(call.message.chat.id, photo, caption=txt, reply_markup=markup)
        except Exception as e:
            print(f"REALME C67 COPY photo error: {e}")
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    elif cd == "dump_model_iphone16_pro_max_copy_mt6735":
        markup = types.InlineKeyboardMarkup(row_width=1)
        photo_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "images",
            "iphone_16_pro_max_copy_mt6735_pandora.jpg",
        )
        try:
            bot.answer_callback_query(call.id)
        except Exception as e:
            print(f"Answer iPhone Copy model callback failed: {e}")
        try:
            bot.delete_message(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
            )
        except Exception as e:
            print(f"Delete iPhone Copy model menu failed: {e}")

        txt = (
            "🍎 iPhone 16 Pro Max Copy - FULL DUMP 🍎\n"
            "━━━━━━━━━━━━\n"
            "📱 Device: iPhone 16 Pro Max Copy\n"
            "🏷️ Model: Pro_Max16 - dream2qltesq\n"
            "🔧 Platform: MT6735 - Build ID NRD90M\n"
            "📱 OS: Android 7.0 - SDK 24\n"
            "🛡️ Patch: 2022-01-05\n"
            "🔖 FW Ver: 1751029924\n"
            "📅 Build Date: 2025-06-27 21:19:38 CST\n"
            "📦 Type: FULL DUMP - Pandora Tool\n"
            "👤 By: Prince Cazanova\n"
            "📦 Size: 1.4GB\n"
            "━━━━━━━━━━━━\n"
            "☁️ Google Drive\n"
            "🔐 Pass: MobiFirmware.VIP\n"
        )
        txt = _dump_card_text(user_id, "dump_model_iphone16_pro_max_copy_mt6735", txt)
        markup.add(types.InlineKeyboardButton(
            _dump_btn(user_id, "📥 Download 1.4GB - Google Drive"),
            url="https://drive.google.com/file/d/1SOhno0YtFUzYGauWnXrr7GIimY6QLHuk/view",
        ))
        markup.add(types.InlineKeyboardButton(
            _dump_back_label(user_id, "⬅️ Back"),
            callback_data="dump_iphone_copy_section",
        ))
        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(
                    call.message.chat.id,
                    photo,
                    caption=txt,
                    reply_markup=markup,
                )
        except Exception as e:
            print(f"Send iPhone Copy model photo failed: {e}")
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    elif cd == "dump_model_iphone_17_pro_copy_ds_bd2":
        lang = hmaxi18n.get_language(user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        gdrive_url = "https://drive.google.com/file/d/1HNXlgyu8pInqB2RLvFQNmaHks8pA7v8-/edit"
        photo_path = "images/iphone_17_pro_copy_ds_bd2.jpg"

        try:
            bot.answer_callback_query(call.id)
        except Exception as e:
            print(f"Answer callback failed: {e}")
        try:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except Exception as e:
            print(f"Delete model menu failed: {e}")

        if lang == "en":
            txt = (
                "🔥 iPhone 17 Pro Copy - ATFELY 🔥\n"
                "━━━━━━━━━━━━\n"
                "📱 Brand: DCODE\n"
                "📱 Device: DS-BD2\n"
                "📌 Model: DS-BD2\n"
                "🔧 Platform: MT6765\n"
                "🔧 Board: k62v1_64_bsp\n"
                "🤖 Android: 12\n"
                "🏗️ Build: SP1A.210812.016\n"
                "🛡️ Patch: 2022-08-01\n"
                "🛠️ Tool: Infinity CM2MT2 v2.53\n"
                "🔐 Pass: MobiFirmware.VIP\n"
            )
            btn_dl = "📥 Download - Google Drive"
            btn_back = "⬅️ Back"
        elif lang == "fr":
            txt = (
                "🔥 iPhone 17 Pro Copy - ATFELY 🔥\n"
                "━━━━━━━━━━━━\n"
                "📱 Marque : DCODE\n"
                "📱 Appareil : DS-BD2\n"
                "📌 Modèle : DS-BD2\n"
                "🔧 Plateforme : MT6765\n"
                "🔧 Carte : k62v1_64_bsp\n"
                "🤖 Android : 12\n"
                "🏗️ Build : SP1A.210812.016\n"
                "🛡️ Correctif : 2022-08-01\n"
                "🛠️ Outil : Infinity CM2MT2 v2.53\n"
                "🔐 Mot de passe : MobiFirmware.VIP\n"
            )
            btn_dl = "📥 Télécharger - Google Drive"
            btn_back = "⬅️ Retour"
        else:
            txt = (
                "🔥 " + "iPh" + "one 17 Pro Copy - ATFELY 🔥\n"
                "━━━━━━━━━━━━\n"
                "📱 العلامة: DCODE\n"
                "📱 الجهاز: DS-BD2\n"
                "📌 الموديل: DS-BD2\n"
                "🔧 المنصة: MT6765\n"
                "🔧 البورد: k62v1_64_bsp\n"
                "🤖 أندرويد: 12\n"
                "🏗️ Build: SP1A.210812.016\n"
                "🛡️ التحديث الأمني: 2022-08-01\n"
                "🛠️ الأداة: Infinity CM2MT2 v2.53\n"
                "🔐 كلمة المرور: MobiFirmware.VIP\n"
            )
            btn_dl = "📥 تحميل - Google Drive"
            btn_back = "⬅️ رجوع"

        markup.add(types.InlineKeyboardButton(btn_dl, url=gdrive_url))
        markup.add(types.InlineKeyboardButton(btn_back, callback_data="dump_copy_full_section"))
        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(call.message.chat.id, photo, caption=txt, reply_markup=markup)
        except Exception as e:
            print(f"Send model photo failed: {e}")
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    elif cd == "dump_model_redmi_a3x_missi_android16":
        markup = types.InlineKeyboardMarkup(row_width=1)
        photo_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "images",
            "redmi_a3x_missi_android16_4.5gb.jpg",
        )
        try:
            bot.answer_callback_query(call.id)
        except Exception as e:
            print(f"Answer Redmi A3x callback failed: {e}")
        try:
            bot.delete_message(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
            )
        except Exception as e:
            print(f"Delete Redmi A3x menu failed: {e}")

        txt = (
            "📱 Xiaomi Redmi A3x - missi - Android 16 Dump 📱\n"
            "━━━━━━━━━━━━\n"
            "🏷️ Product: missi - Redmi A3x\n"
            "📦 File: Full Dump - Android 16\n"
            "🔧 Tool: AMT Tool\n"
            "📦 Size: 4.5GB\n"
            "👤 Thanks: Abdessamad Sbai\n"
            "━━━━━━━━━━━━\n"
            "📱 Specs: Unisoc T603 Octa 1.8GHz PowerVR GE8322\n"
            "💾 RAM: 3/4GB LPDDR4X - 64/128GB eMMC 5.1\n"
            "📱 Display: 6.71 HD+ 1650x720 90Hz\n"
            "📸 8MP / 5MP - 5000mAh 10W USB-C\n"
            "🔧 Side Fingerprint - Dual SIM + microSD\n"
            "📱 Original OS: Android 14\n"
            "━━━━━━━━━━━━\n"
            "☁️ Upload: Google Drive\n"
            "🔐 Pass: MobiFirmware.VIP\n"
        )
        txt = _dump_card_text(user_id, "dump_model_redmi_a3x_missi_android16", txt)
        markup.add(types.InlineKeyboardButton(
            _dump_btn(user_id, "📥 Download 4.5GB - Google Drive"),
            url="https://drive.google.com/file/d/1Xxx7HG60lnaXQft27RdCmvzresdbppBb/view",
        ))
        markup.add(types.InlineKeyboardButton(
            _dump_back_label(user_id, "⬅️ Back"),
            callback_data="dump_xiaomi_group_section",
        ))
        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(
                    call.message.chat.id,
                    photo,
                    caption=txt,
                    reply_markup=markup,
                )
        except Exception as e:
            print(f"Send Redmi A3x photo failed: {e}")
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    elif cd == "dump_model_redmi_note14_5g_beryl_xml":
        markup = types.InlineKeyboardMarkup(row_width=1)
        photo_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "images",
            "redmi_note14_5g_beryl_xml_6_5gb_easy_jtag.jpg",
        )
        gdrive_url = "https://drive.google.com/file/d/1zxRGj8wgYfsDQaVfn7RB53Xw78JmCToF/view"
        try:
            bot.answer_callback_query(call.id)
        except Exception as e:
            print(f"Answer Redmi Note 14 5G Beryl callback failed: {e}")
        try:
            bot.delete_message(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
            )
        except Exception as e:
            print(f"Delete Redmi Note 14 5G Beryl menu failed: {e}")

        txt = (
            "📱 Redmi Note 14 5G — Beryl — XML FULL DUMP 🔥\n"
            "━━━━━━━━━━━━\n"
            "النهارده بنقدم لكم XML FULL DUMP للجهاز، مسحوب بالعملاق:\n"
            "🔧 Easy JTAG Plus\n"
            "━━━━━━━━━━━━\n"
            "📱 Device: Redmi Note 14 5G — Beryl\n"
            "📁 نوع الملف: XML FULL DUMP\n"
            "📦 حجم الدامب: 6.5 GB\n"
            "☁️ مرفوع على: Google Drive\n"
            "🔐 Pass File: MobiFirmware.VIP\n"
            "━━━━━━━━━━━━\n"
            "💾 دامب بحجم 6.5 جيجا ومجهز للفنيين للتعامل\n"
            "مع حالات الجهاز وعمليات التفليش.\n"
        )
        txt = _dump_card_text(user_id, "dump_model_redmi_note14_5g_beryl_xml", txt)
        markup.add(types.InlineKeyboardButton(
            _dump_btn(user_id, "📥 Download 6.5GB - Google Drive"),
            url=gdrive_url,
        ))
        markup.add(types.InlineKeyboardButton(
            _dump_back_label(user_id, "⬅️ Back"),
            callback_data="dump_xiaomi_group_section",
        ))
        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(
                    call.message.chat.id,
                    photo,
                    caption=txt,
                    reply_markup=markup,
                )
        except Exception as e:
            print(f"Send Redmi Note 14 5G Beryl photo failed: {e}")
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    elif cd == "dump_model_redmi_10a_220233l2g":
        lang = hmaxi18n.get_language(user_id)
        contact_footer = {
            "ar": (
                "⚠️ حقوق HMAX - هيثم ماكس\n"
                "📱 واتساب: https://wa.me/message/A3KQWHSSERCFG1\n"
                "📘 فيسبوك: https://www.facebook.com/share/1C3JnWP5bM/\n"
                "✈️ تيليجرام: @hithammax"
            ),
            "en": (
                "⚠️ HMAX - Haitham Max Copyright Notice\n"
                "📱 WhatsApp: https://wa.me/message/A3KQWHSSERCFG1\n"
                "📘 Facebook: https://www.facebook.com/share/1C3JnWP5bM/\n"
                "✈️ Telegram: @hithammax"
            ),
            "fr": (
                "⚠️ Droits d'auteur HMAX - Haitham Max\n"
                "📱 WhatsApp : https://wa.me/message/A3KQWHSSERCFG1\n"
                "📘 Facebook : https://www.facebook.com/share/1C3JnWP5bM/\n"
                "✈️ Telegram : @hithammax"
            ),
        }.get(lang, "⚠️ HMAX - Haitham Max Copyright Notice\n📱 WhatsApp: https://wa.me/message/A3KQWHSSERCFG1\n📘 Facebook: https://www.facebook.com/share/1C3JnWP5bM/\n✈️ Telegram: @hithammax")
        if lang == "en":
            display_text = (
                "🔥 XIAOMI REDMI 10A 220233L2G | 64GB eMMC FULL DUMP\n"
                "📱 Model: 220233L2G\n"
                "💾 Storage: 64GB eMMC\n"
                "🔖 Version: V12.5.3.0.RCZMIXM\n"
                "🛠️ Dumped With: F64 ULTRA\n"
                "📏 Size: 2.5 GB\n\n"
                "🔑 PASS: MobiFirmware.VIP"
            )
            download_label = "📥 Download Link"
            back = "🔙 Back to Redmi DUMPs"
        elif lang == "fr":
            display_text = (
                "🔥 DUMP COMPLET XIAOMI REDMI 10A 220233L2G | 64GB eMMC\n"
                "📱 Modèle : 220233L2G\n"
                "💾 Stockage : 64GB eMMC\n"
                "🔖 Version : V12.5.3.0.RCZMIXM\n"
                "🛠️ Extrait avec : F64 ULTRA\n"
                "📏 Taille : 2.5 GB\n\n"
                "🔑 MOT DE PASSE : MobiFirmware.VIP"
            )
            download_label = "📥 Lien de téléchargement"
            back = "🔙 Retour aux DUMP Redmi"
        else:
            display_text = (
                "🔥 دامب كامل XIAOMI REDMI 10A 220233L2G | 64GB eMMC\n"
                "📱 الموديل: 220233L2G\n"
                "💾 التخزين: 64GB eMMC\n"
                "🔖 الإصدار: V12.5.3.0.RCZMIXM\n"
                "🛠️ تم السحب بواسطة: F64 ULTRA\n"
                "📏 الحجم: 2.5 GB\n\n"
                "🔑 كلمة المرور: MobiFirmware.VIP"
            )
            download_label = "📥 رابط التحميل"
            back = "🔙 رجوع إلى دامبات ريدمي"

        display_text = f"{display_text}\n\n{contact_footer}"
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton(
            download_label,
            url="https://drive.google.com/file/d/1ApV1GSSHo74SnIgm7rQEYxrmx673uoTP",
        ))
        markup.add(types.InlineKeyboardButton(back, callback_data="dump_xiaomi_group_section"))
        bot.edit_message_text(
            display_text,
            user_id,
            call.message.message_id,
            reply_markup=markup,
        )
        return

    elif cd == "dump_model_redmi_15c_poco_c85":
        lang = hmaxi18n.get_language(user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        photo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", "redmi_15c.jpg")
        gdrive_url = "https://drive.google.com/file/d/1ztxrctjJJLCoQq6a0ka7FWm_SRal1hwz/view"

        try:
            bot.answer_callback_query(call.id)
        except:
            pass
        try:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except:
            pass

        if lang == "en":
            txt = (
                "🔥 XIAOMI REDMI 15C / POCO C85 DUMP FILE 🔥\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                "📱 Models: REDMI 15C | POCO C85\n"
                "💾 Storage: 256GB EMMC\n"
                "📂 File Type: DUMP FILE\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                "💿 DUMP INFORMATION\n"
                "📌 Version: AP3A.240905.015.A2 OS2.0.221.0.VBNMIXM\n"
                "🛠️ Dumped With: F64 ULTRA\n"
                "📏 Size: 7.4 GB\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                "Uploaded By: Reynold Bermil Leonido\n"
                "Dumping-Firmware\n"
                "☁️ Google Drive\n"
                "🔐 Password: MobiFirmware.VIP\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                "📞 https://wa.me/message/A3KQWHSSERCFG1\n"
            )
        else:
            txt = (
                "🔥 دامب شاومي ريدمي 15C / بوكو C85 🔥\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                "📱 الموديلات: REDMI 15C | POCO C85\n"
                "💾 التخزين: 256GB EMMC\n"
                "📂 نوع الملف: DUMP FILE\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                "📌 الإصدار: AP3A.240905.015.A2 OS2.0.221.0.VBNMIXM\n"
                "🛠️ السحب: F64 ULTRA\n"
                "📏 الحجم: 7.4 GB\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                "Uploaded By: Reynold Bermil Leonido\n"
                "☁️ Google Drive\n"
                "🔐 كلمة المرور: MobiFirmware.VIP\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                "📞 https://wa.me/message/A3KQWHSSERCFG1\n"
            )
        txt = _dump_card_text(user_id, "dump_model_redmi_15c_poco_c85", txt)

        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📥 Download - Google Drive"), url=gdrive_url))
        markup.add(types.InlineKeyboardButton(_dump_back_label(user_id, "🔙 Back"), callback_data="dump_xiaomi_group_section"))
        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(call.message.chat.id, photo)
        except OSError as e:
            print(f"Failed to open Redmi 15C image {photo_path}: {e}")
        except Exception as e:
            print(f"Failed to send Redmi 15C image: {e}")
        bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    elif cd == "dump_model_redmi_a3_c61":
        markup = types.InlineKeyboardMarkup(row_width=1)
        gdrive_url = "https://drive.google.com/file/d/1R-6hqUPVx5k5Y5l5Umws2-f0fXZNKOHi/view"

        try:
            bot.answer_callback_query(call.id)
        except:
            pass
        try:
            bot.delete_message(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
            )
        except:
            pass

        txt = (
            "🔥 XIAOMI REDMI A3 C61 FULL DUMP 🔥\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "📱 Device: REDMI A3 C61\n"
            "💾 Storage: 64GB\n"
            "📂 File: FULL DUMP\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "💿 DUMP INFORMATION\n"
            "📌 Version: 16.V816.0.7.0.WGRMIXM\n"
            "🛠️ Dumped With: F64 ULTRA\n"
            "📏 Size: 3.6 GB\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "☁️ Google Drive\n"
            "🔐 Password: MobiFirmware.VIP\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "📞 https://wa.me/message/A3KQWHSSERCFG1\n"
        )
        txt = _dump_card_text(user_id, "dump_model_redmi_a3_c61", txt)

        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📥 Download - Google Drive"), url=gdrive_url))
        markup.add(types.InlineKeyboardButton(_dump_back_label(user_id, "🔙 Back"), callback_data="dump_xiaomi_group_section"))
        bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    elif cd == "dump_model_redmi_9c_m2006c3mg":
        lang = hmaxi18n.get_language(user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        gdrive_url = "https://drive.google.com/file/d/1YxY9QvJq62wAR88VcZSIrlh6q0BMx9Ui/view"

        try:
            bot.answer_callback_query(call.id)
        except:
            pass
        try:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except:
            pass

        if lang == "en":
            txt = (
                "🔥 XIAOMI REDMI 9C - M2006C3MG DUMP FILE 🔥\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                "📱 Model: XIAOMI REDMI 9C\n"
                "🔢 Model Number: M2006C3MG\n"
                "📂 File Type: DUMP FILE\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                "💾 DUMP INFORMATION\n"
                "🛠️ Dumped With: EASY JTAG PLUS\n"
                "📏 Dump Size: 3 GB\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                "Uploaded By: Reynold Bermil Leonido\n"
                "Dumping-Firmware\n"
                "☁️ Google Drive\n"
                "🔐 Password: MobiFirmware.VIP\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                "📞 https://wa.me/message/A3KQWHSSERCFG1\n"
            )
        else:
            txt = (
                "🔥 شاومي ريدمي 9C M2006C3MG - ملف دامب 🔥\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                "📱 الموديل: XIAOMI REDMI 9C\n"
                "🔢 رقم الموديل: M2006C3MG\n"
                "📂 نوع الملف: DUMP FILE\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                "💾 معلومات الدامب\n"
                "🛠️ تم السحب بواسطة: EASY JTAG PLUS\n"
                "📏 حجم الدامب: 3 GB\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                "Uploaded By: Reynold Bermil Leonido\n"
                "☁️ Google Drive\n"
                "🔐 كلمة المرور: MobiFirmware.VIP\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                "📞 https://wa.me/message/A3KQWHSSERCFG1\n"
            )
        txt = _dump_card_text(user_id, "dump_model_redmi_9c_m2006c3mg", txt)

        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📥 Download - Google Drive"), url=gdrive_url))
        markup.add(types.InlineKeyboardButton(_dump_back_label(user_id, "🔙 Back"), callback_data="dump_xiaomi_group_section"))
        bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    elif cd == "dump_model_redmi_13c_gale":
        lang = hmaxi18n.get_language(user_id)
        terabox_url = "https://www.terabox.app/arabic/sharing/link?surl=h5bhksix3MWtLXRftpknUQ"
        photo_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "images",
            "xiaomi_redmi_13c_gale_os2_hmax.jpg",
        )
        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass
        try:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except Exception:
            pass

        txts = {
            "ar": (
                "🔥 XIAOMI Redmi 13C (Gale) OS2.0.6.0.VGPMIXM 🔥\n"
                "━━━━━━━━━━━━\n"
                "📱 Model: Redmi 13C (Gale)\n"
                "🔖 Version: OS2.0.6.0.VGPMIXM\n"
                "🛠️ Dump BY PANDORA\n"
                "📂 Type: Full Dump\n"
                "🔑 Pass File: MobiFirmware.VIP\n"
                "☁️ Server: Terabox\n"
                "━━━━━━━━━━━━\n"
                "⚠️ ملاحظه مهمه لازم تفتح VPN سايفون على شان تفتح صفحه التحميل\n"
                "━━━━━━━━━━━━\n"
                "HMAX-UNLOCKER - HithamMax"
            ),
            "en": (
                "🔥 XIAOMI Redmi 13C (Gale) OS2.0.6.0.VGPMIXM 🔥\n"
                "📱 Model: Redmi 13C (Gale)\n"
                "🔖 Version: OS2.0.6.0.VGPMIXM\n"
                "🛠️ Dump BY PANDORA\n"
                "📂 Type: Full Dump\n"
                "🔑 Password: MobiFirmware.VIP\n"
                "☁️ Server: Terabox\n"
                "⚠️ Important: Open Psiphon VPN to open download page\n"
                "HMAX-UNLOCKER"
            ),
            "fr": (
                "🔥 XIAOMI Redmi 13C (Gale) OS2.0.6.0.VGPMIXM 🔥\n"
                "📱 Modèle: Redmi 13C (Gale)\n"
                "🔖 Version: OS2.0.6.0.VGPMIXM\n"
                "🛠️ Dump par PANDORA\n"
                "📂 Type: Full Dump\n"
                "🔑 Mot de passe: MobiFirmware.VIP\n"
                "☁️ Serveur: Terabox\n"
                "⚠️ Important: Ouvrez VPN Psiphon pour ouvrir la page\n"
                "HMAX-UNLOCKER"
            ),
        }
        txt = txts.get(lang, txts["ar"])
        btn_dl = {"ar": "📥 تحميل من Terabox - VPN سايفون مطلوب", "en": "📥 Download Terabox - Need VPN", "fr": "📥 Télécharger Terabox - VPN requis"}.get(lang, "📥 تحميل من Terabox - VPN سايفون مطلوب")
        btn_back = {"ar": "⬅️ رجوع لـ XIAOMI", "en": "⬅️ Back to XIAOMI", "fr": "⬅️ Retour à XIAOMI"}.get(lang, "⬅️ رجوع لـ XIAOMI")

        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton(btn_dl, url=terabox_url))
        markup.add(types.InlineKeyboardButton(btn_back, callback_data="dump_xiaomi_group_section"))
        try:
            with open(photo_path, "rb") as p:
                bot.send_photo(call.message.chat.id, p, caption=txt, reply_markup=markup)
        except Exception:
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    elif cd == "dump_zte_full_section":
        lang = hmaxi18n.get_language(user_id)
        translations = {
            "ar": {
                "title": "🗄️ دامبات ZTE الكاملة",
                "model": "📱 ZTE BLADE V70 MAX (Z2467) - 6.1GB",
                "back": "🔙 رجوع إلى أقسام الدامب",
            },
            "en": {
                "title": "🗄️ ZTE Full DUMPs",
                "model": "📱 ZTE BLADE V70 MAX (Z2467) - 6.1GB",
                "back": "🔙 Back to DUMP categories",
            },
            "fr": {
                "title": "🗄️ DUMP complets ZTE",
                "model": "📱 ZTE BLADE V70 MAX (Z2467) - 6.1GB",
                "back": "🔙 Retour aux catégories DUMP",
            },
        }
        labels = translations.get(lang, translations["ar"])
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton(
            labels["model"],
            callback_data="dump_model_zte_v70_max_z2467",
        ))
        markup.add(types.InlineKeyboardButton(labels["back"], callback_data="dump_main_section"))
        _hmax_show_menu(call, labels["title"], markup)
        return

    elif cd == "dump_model_zte_v70_max_z2467":
        lang = hmaxi18n.get_language(user_id)
        translations = {
            "ar": {
                "details": (
                    "🔥 دامب كامل ZTE BLADE V70 MAX (Z2467)\n"
                    "📱 الموديل: Z2467\n"
                    "🔖 الإصدار: MyOS15.0.3_Z2467_AS1\n"
                    "🛠️ تم السحب بواسطة: UNLOCKTOOL\n"
                    "📏 الحجم: 6.1 GB\n"
                    "🔑 كلمة المرور: MobiFirmware.VIP"
                ),
                "footer": (
                    "⚠️ حقوق HMAX - هيثم ماكس\n"
                    "📱 واتساب: https://wa.me/message/A3KQWHSSERCFG1\n"
                    "📘 فيسبوك: https://www.facebook.com/share/1C3JnWP5bM/\n"
                    "✈️ تيليجرام: @hithammax"
                ),
                "download": "📥 تحميل",
                "back": "🔙 رجوع إلى دامبات ZTE",
            },
            "en": {
                "details": (
                    "🔥 ZTE BLADE V70 MAX (Z2467) FULL DUMP\n"
                    "📱 Model: Z2467\n"
                    "🔖 Version: MyOS15.0.3_Z2467_AS1\n"
                    "🛠️ Dumped With: UNLOCKTOOL\n"
                    "📏 Size: 6.1 GB\n"
                    "🔑 PASS: MobiFirmware.VIP"
                ),
                "footer": (
                    "⚠️ HMAX - Haitham Max Copyright Notice\n"
                    "📱 WhatsApp: https://wa.me/message/A3KQWHSSERCFG1\n"
                    "📘 Facebook: https://www.facebook.com/share/1C3JnWP5bM/\n"
                    "✈️ Telegram: @hithammax"
                ),
                "download": "📥 Download",
                "back": "🔙 Back to ZTE DUMPs",
            },
            "fr": {
                "details": (
                    "🔥 DUMP COMPLET ZTE BLADE V70 MAX (Z2467)\n"
                    "📱 Modèle : Z2467\n"
                    "🔖 Version : MyOS15.0.3_Z2467_AS1\n"
                    "🛠️ Extrait avec : UNLOCKTOOL\n"
                    "📏 Taille : 6.1 GB\n"
                    "🔑 MOT DE PASSE : MobiFirmware.VIP"
                ),
                "footer": (
                    "⚠️ Droits d'auteur HMAX - Haitham Max\n"
                    "📱 WhatsApp : https://wa.me/message/A3KQWHSSERCFG1\n"
                    "📘 Facebook : https://www.facebook.com/share/1C3JnWP5bM/\n"
                    "✈️ Telegram : @hithammax"
                ),
                "download": "📥 Télécharger",
                "back": "🔙 Retour aux DUMP ZTE",
            },
        }
        labels = translations.get(lang, translations["ar"])
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton(
            labels["download"],
            url="https://drive.google.com/file/d/1FYp9WGh_4o7ycHVaQzC1iB6s_LNjByGr/view",
        ))
        markup.add(types.InlineKeyboardButton(
            labels["back"],
            callback_data="dump_zte_full_section",
        ))
        bot.edit_message_text(
            f'{labels["details"]}\n\n{labels["footer"]}',
            user_id,
            call.message.message_id,
            reply_markup=markup,
        )
        return

    elif cd in ("dump_huawei_section", "dump_huawei_honor_section"):
        lang = hmaxi18n.get_language(user_id)
        section_labels = {
            "ar": {
                "title": "🗄️ *HUAWEI & HONOR DUMP FILES*\n\nاختر الموديل:",
                "model": "📱 HONOR X7A RKY-LX2 - FULL DUMP UFI",
                "new_region": "🔥 50 Lite NTN-L22 C185 - New Region [UnlockTool]",
                "back": "🔙 رجوع",
            },
            "en": {
                "title": "🗄️ *HUAWEI & HONOR DUMP FILES*",
                "model": "📱 HONOR X7A RKY-LX2 - FULL DUMP UFI",
                "new_region": "🔥 50 Lite NTN-L22 C185 - New Region [UnlockTool]",
                "back": "🔙 Back",
            },
            "fr": {
                "title": "🗄️ *FICHIERS DUMP HUAWEI & HONOR*\n\nChoisissez le modèle :",
                "model": "📱 HONOR X7A RKY-LX2 - FULL DUMP UFI",
                "new_region": "🔥 50 Lite NTN-L22 C185 - New Region [UnlockTool]",
                "back": "🔙 Retour",
            },
        }
        labels = section_labels.get(lang, section_labels["ar"])
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton(
            _dump_btn(user_id, "🔥 Y7A PPA-LX2 - EASY JTAG PLUS"),
            callback_data="dump_model_huawei_y7a_ppa_lx2",
        ))
        markup.add(types.InlineKeyboardButton(
            _dump_btn(user_id, "🔥 X7B CLK-LX2 C185 - UnlockTool"),
            callback_data="dump_model_honor_x7b_clk_lx2",
        ))
        markup.add(types.InlineKeyboardButton(
            _dump_btn(user_id, "🔥 400 ABR-N03 OSv15 FULL [F64 ULTRA]"),
            callback_data="dump_model_honor_400_abr_n03_osv15",
        ))
        markup.add(types.InlineKeyboardButton(
            labels["new_region"],
            callback_data="dump_model_honor_50_lite_ntn_l22_new",
        ))
        markup.add(types.InlineKeyboardButton(
            labels["model"],
            callback_data="dump_model_honor_x7a_rky_lx2",
        ))
        markup.add(types.InlineKeyboardButton(
            labels["back"],
            callback_data="dump_main_section",
        ))
        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass
        # Return to the merged menu from either a text or photo detail message.
        try:
            bot.delete_message(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
            )
        except Exception:
            pass
        bot.send_message(
            call.message.chat.id,
            labels["title"],
            reply_markup=markup,
            parse_mode="Markdown",
        )
        return

    elif cd == "dump_model_huawei_y7a_ppa_lx2":
        markup = types.InlineKeyboardMarkup(row_width=1)
        gdrive_url = "https://drive.google.com/file/d/1R5Rku8E4MN3t4miBfgGLIcVxqPVYX6iP/view"
        photo_path = "images/huawei_y7a_ppa_lx2.jpg"
        try:
            bot.answer_callback_query(call.id)
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except:
            pass
        txt = (
            "📱 HUAWEI Y7A - DUMP FILE 📱\n"
            "━━━━━━━━━━━━\n"
            "📱 Device: HUAWEI Y7A\n"
            "🏷️ Model: PPA-LX2\n"
            "🔧 Dump By: EASY JTAG PLUS\n"
            "👨‍🔧 Uploaded By: Eng. Reynold Bermil Leonido\n"
            "☁️ Upload: Google Drive\n"
            "━━━━━━━━━━━━\n"
            "🔐 Pass: MobiFirmware.VIP\n"
        )
        txt = _dump_card_text(user_id, "dump_model_huawei_y7a_ppa_lx2", txt)
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📥 Download - Google Drive"), url=gdrive_url))
        markup.add(types.InlineKeyboardButton(_dump_back_label(user_id, "⬅️ Back"), callback_data="dump_huawei_section"))
        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(call.message.chat.id, photo, caption=txt, reply_markup=markup)
        except:
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    elif cd == "dump_model_honor_x7b_clk_lx2":
        markup = types.InlineKeyboardMarkup(row_width=1)
        gdrive_url = "https://drive.google.com/file/d/1C2dhyqDx6WA7gb3VXcaYwG4PTQ5NweRM/view"
        photo_path = "images/honor_x7b_clk_lx2_c185.jpg"
        try:
            bot.answer_callback_query(call.id)
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except:
            pass
        txt = (
            "📱 Honor X7B - FULL DUMP 📱\n"
            "━━━━━━━━━━━━\n"
            "📱 Device: Honor X7B\n"
            "🏷️ Model: CLK-LX2 / C185\n"
            "📁 File: Full Dump\n"
            "🔧 Read By: UnlockTool\n"
            "☁️ Upload: Google Drive\n"
            "━━━━━━━━━━━━\n"
            "⚠️ تأكد من تطابق الموديل والذاكرة وحالة البورد قبل الكتابة\n"
            "🔐 Pass: MobiFirmware.VIP\n"
        )
        txt = _dump_card_text(user_id, "dump_model_honor_x7b_clk_lx2", txt)
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📥 Download - Google Drive"), url=gdrive_url))
        markup.add(types.InlineKeyboardButton(_dump_back_label(user_id, "⬅️ Back"), callback_data="dump_huawei_section"))
        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(call.message.chat.id, photo, caption=txt, reply_markup=markup)
        except:
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    elif cd == "dump_model_honor_400_abr_n03_osv15":
        markup = types.InlineKeyboardMarkup(row_width=1)
        gdrive_url = "https://drive.google.com/file/d/1beAVNfe4wY31rb8xfjz41hVWOxX7npqn/view"
        photo_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "images",
            "honor_400_abr_n03_osv15_full_dump_f64_ultra.jpg",
        )
        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass
        try:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except Exception:
            pass
        txt = (
            "⭐ HONOR 400 — ABR-N03 — FULL DUMP | OSv15 🔥\n"
            "━━━━━━━━━━━━\n"
            "📁 Firmware:\n"
            "HONOR 400 - ABR-N03 9.0.0.213(C69E5R1P1)\n"
            "OSv15 FULL DUMP\n"
            "━━━━━━━━━━━━\n"
            "⚡ Pulled By:\n"
            "F64 ULTRA\n"
            "━━━━━━━━━━━━\n"
            "📱 Device: HONOR 400 ABR-N03\n"
            "🔢 Version: 9.0.0.213(C69E5R1P1)\n"
            "🟡 OS: OSv15 - FULL DUMP\n"
            "🔧 Tool: F64 ULTRA\n"
            "☁️ Hosting: Google Drive\n"
            "🔐 Pass File: MobiFirmware.VIP\n"
        )
        txt = _dump_card_text(user_id, "dump_model_honor_400_abr_n03_osv15", txt)
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📥 Download - Google Drive"), url=gdrive_url))
        markup.add(types.InlineKeyboardButton(_dump_back_label(user_id, "⬅️ Back"), callback_data="dump_huawei_section"))
        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(call.message.chat.id, photo, caption=txt, reply_markup=markup)
        except Exception as e:
            print(f"Send HONOR 400 photo failed: {e}")
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    elif cd == "dump_model_honor_50_lite_ntn_l22_new":
        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass
        try:
            bot.delete_message(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
            )
        except Exception as e:
            print(f"Delete HONOR 50 Lite menu failed: {e}")

        txt = (
            "📱 Honor 50 Lite - NEW REGION C185 📱\n"
            "━━━━━━━━━━━━\n"
            "📱 Device: Honor 50 Lite\n"
            "🏷️ Model: NTN-L22 | C185\n"
            "🌍 Tawjih: C185 - توجيه مختلف - متاح للجميع\n"
            "🔧 Dump By: Unlock Tool\n"
            "✅ Status: مسحوب بالـ Unlock Tool - جاهز للتفليش\n"
            "💡 يمكن تفليشه بواسطة أي Tool تدعم هذا النوع\n"
            "🎁 هدية مجانية للفنيين\n"
            "☁️ Upload: Google Drive\n"
            "━━━━━━━━━━━━\n"
            "🔐 Pass: MobiFirmware.VIP"
        )
        txt = _dump_card_text(user_id, "dump_model_honor_50_lite_ntn_l22_new", txt)
        photo_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "images",
            "honor_50_lite_ntn_l22_c185_new.jpg",
        )
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton(
            _dump_btn(user_id, "📥 Download - Google Drive"),
            url="https://drive.google.com/file/d/1V977zxhIp-2bDbiaDWD07wTrKyRiU11Z/view",
        ))
        markup.add(types.InlineKeyboardButton(
            _dump_back_label(user_id, "⬅️ Back"),
            callback_data="dump_huawei_section",
        ))
        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(
                    call.message.chat.id,
                    photo,
                    caption=txt,
                    reply_markup=markup,
                )
        except Exception as e:
            print(f"Send HONOR 50 Lite photo failed: {e}")
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    elif cd == "dump_model_honor_x7a_rky_lx2":
        try:
            bot.answer_callback_query(call.id, text={"en": "⏳ Loading...", "fr": "⏳ Chargement..."}.get(hmaxi18n.get_language(user_id), "جاري التحميل..."))
        except Exception:
            pass

        try:
            bot.delete_message(user_id, call.message.message_id)
        except Exception as e:
            print(f"Failed to delete old HONOR dump menu: {e}")

        try:
            bot.copy_message(chat_id=call.message.chat.id, from_chat_id="@HMAX_FILE", message_id=4)
        except Exception as e:
            print(f"Copy 4 failed: {e}")
        try:
            bot.copy_message(chat_id=call.message.chat.id, from_chat_id="@HMAX_FILE", message_id=5)
        except Exception as e:
            print(f"Copy 5 failed: {e}")

        lang = hmaxi18n.get_language(user_id)
        detail_translations = {
            "ar": {
                "details": (
                    "🔥 *دامب هونور X7A RKY-LX2 كامل باليوفي*\n"
                    "━━━━━━━━━━━━\n"
                    "📱 الموديل: RKY-LX2\n"
                    "🔖 الإصدار: RKY-L32 6.1.0.203\n"
                    "🛠️ السحب: UFI\n"
                    "⚠️ ملاحظة: Boot Config = 0x48\n"
                    "🔑 الباسورد: Melok@AbouAmr\n"
                    "━━━━━━━━━━━━\n"
                    "💎 HMAX"
                ),
                "footer": (
                    "⚠️ حقوق HMAX - هيثم ماكس\n"
                    "📱 واتساب: https://wa.me/message/A3KQWHSSERCFG1\n"
                    "📘 فيسبوك: https://www.facebook.com/share/1C3JnWP5bM/\n"
                    "✈️ تيليجرام: @hithammax"
                ),
                "download": "📥 رابط التحميل - Mediafire",
                "back": "🔙 رجوع لهونور",
            },
            "en": {
                "details": (
                    "🔥 *HONOR X7A - RKY-LX2 FULL DUMP by UFI*\n"
                    "📱 Model: RKY-LX2\n"
                    "🔖 FW: RKY-L32 6.1.0.203\n"
                    "🛠️ Dumped with: UFI\n"
                    "⚠️ Boot Config = 0x48\n"
                    "🔑 PASS: Melok@AbouAmr"
                ),
                "footer": (
                    "⚠️ HMAX - Haitham Max Copyright Notice\n"
                    "📱 WhatsApp: https://wa.me/message/A3KQWHSSERCFG1\n"
                    "📘 Facebook: https://www.facebook.com/share/1C3JnWP5bM/\n"
                    "✈️ Telegram: @hithammax"
                ),
                "download": "📥 Download - Mediafire",
                "back": "🔙 Back to HONOR",
            },
            "fr": {
                "details": (
                    "🔥 *DUMP COMPLET HONOR X7A RKY-LX2 par UFI*\n"
                    "📱 Modèle : RKY-LX2\n"
                    "🔖 Firmware : RKY-L32 6.1.0.203\n"
                    "🛠️ Extrait avec : UFI\n"
                    "⚠️ Configuration de démarrage = 0x48\n"
                    "🔑 MOT DE PASSE : Melok@AbouAmr"
                ),
                "footer": (
                    "⚠️ Droits d'auteur HMAX - Haitham Max\n"
                    "📱 WhatsApp : https://wa.me/message/A3KQWHSSERCFG1\n"
                    "📘 Facebook : https://www.facebook.com/share/1C3JnWP5bM/\n"
                    "✈️ Telegram : @hithammax"
                ),
                "download": "📥 Télécharger - Mediafire",
                "back": "🔙 Retour à HONOR",
            },
        }
        labels = detail_translations.get(lang, detail_translations["ar"])
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton(
            labels["download"],
            url="https://www.mediafire.com/file/ldl8120aynxzlhx/honor_x7a_RKY-LX2_full_dump_by_UFI.rar/file",
        ))
        markup.add(types.InlineKeyboardButton(
            labels["back"],
            callback_data="dump_huawei_section",
        ))
        bot.send_message(
            user_id,
            f'{labels["details"]}\n\n{labels["footer"]}',
            reply_markup=markup,
            parse_mode="Markdown",
        )
        return

    # ===== 💾 تفاصيل Google Pixels Dump =====
    elif cd == "dump_pixel_section":
        try: bot.answer_callback_query(call.id)
        except: pass
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton(_dump_btn(user_id, "📱 Pixel 6"), url="https://drive.google.com/file/d/1t-UkvyGDULYjzvGrTektcXfdyef9rx5X/view?usp=drivesdk"),
            types.InlineKeyboardButton(_dump_btn(user_id, "📱 Pixel 6A"), url="https://drive.google.com/file/d/1SGVfpVjN6NhilYsfbRtBgY1OYTy1eCWa/view?usp=drivesdk"),
            types.InlineKeyboardButton(_dump_btn(user_id, "📱 Pixel 6 Pro"), url="https://drive.google.com/file/d/1o1YXHa6VOJHHgqby-TmsJ7guUZDvHPNA/view?usp=drivesdk"),
            types.InlineKeyboardButton(_dump_btn(user_id, "📱 Pixel 7 (BlackMan V2)"), url="https://drive.google.com/file/d/1WEbLeY_TjhI-sH1VTo1HB95jkKcS3j_d/view?usp=drivesdk"),
            types.InlineKeyboardButton(_dump_btn(user_id, "📱 Pixel 7A"), url="https://drive.google.com/file/d/1VLjoddVR-zV0N-MEYoYSabEDwpXmU4LA/view?usp=drivesdk"),
            types.InlineKeyboardButton(_dump_btn(user_id, "📱 Pixel 7 Pro"), url="https://drive.google.com/file/d/13REk97lBoxKKCrXdrrozRFyvp--x9j4I/view?usp=drivesdk"),
            types.InlineKeyboardButton(_dump_btn(user_id, "📱 Tibuta Tab 868 pro DUMP"), callback_data="dump_tibuta_868"),
            types.InlineKeyboardButton(_dump_btn(user_id, "🔙 رجوع"), callback_data="dump_main_section")
        )
        
        display_text = (
            "💾 **ملفات الـ DUMP - Google Pixels:**\n\n"
            "هنا تجد ملفات الدامب المختارة بعناية لأجهزة بكسل.\n\n"
            "⚠️ **حقوق النشر:**\n"
            "جميع الحقوق محفوظة لدى: @HMAX_UNLOCKER_bot"
        )
        _hmax_show_menu(call, display_text, markup, parse_mode="Markdown")
        return

    # ===== 📁 تفاصيل ملف DUMP لهاتف H-HORSE M16 PRO MAX =====
    elif cd == "dump_h_horse_m16":
        try: bot.answer_callback_query(call.id)
        except: pass

        lang = hmaxi18n.get_language(user_id)
        h_horse_translations = {
            "ar": {
                "details": (
                    "📱 **ملف DUMP لهاتف H-HORSE M16 PRO MAX**\n"
                    "━━━━━━━━━━━━━━━━━━\n"
                    "🌹 **شكر خاص:**\n"
                    "للأخ أبو عبدالسلام والأخ نجيب (صاحب مجتمع برمجة موبايل في التيليجرام) على توفير هذا الملف.\n\n"
                    "⚠️ **تنبيه هام جداً:**\n"
                    "معالج هذا الهاتف (SPD) ضعيف وحساس. **نصيحة أخوية:** قم بسحب نسخة DUMP احتياطية من الهاتف قبل البدء بعملية التفليش لتجنب فقدان البوت (Boot).\n\n"
                    "🔐 **كلمات السر المحتملة لفك الضغط (جربها بالترتيب):**\n"
                    "1. `1234`\n"
                    "2. `12345678`\n"
                    "3. `[www.khulnafirmwarer.com]`\n"
                    "4. `www.khulnafirmwarer.com`\n"
                    "5. `khulnafirmwarer.com`\n"
                    "6. `Gsm King Khulna`\n"
                    "━━━━━━━━━━━━━━━━━━"
                ),
                "download": "📥 رابط تحميل الفلاشة",
                "back": "🔙 العودة لقائمة M-HORSE DUMP",
            },
            "en": {
                "details": (
                    "📱 **DUMP File for H-HORSE M16 PRO MAX**\n"
                    "━━━━━━━━━━━━━━━━━━\n"
                    "🌹 **Special Thanks:**\n"
                    "To brother Abu Abdelsalam and brother Naguib (owner of the Mobile Programming community on Telegram) for providing this file.\n\n"
                    "⚠️ **Very Important Warning:**\n"
                    "This device chipset (SPD) is weak and sensitive. **Friendly advice:** take a backup DUMP of the phone before starting the flashing process to avoid losing the boot.\n\n"
                    "🔐 **Possible extraction passwords (try them in order):**\n"
                    "1. `1234`\n"
                    "2. `12345678`\n"
                    "3. `[www.khulnafirmwarer.com]`\n"
                    "4. `www.khulnafirmwarer.com`\n"
                    "5. `khulnafirmwarer.com`\n"
                    "6. `Gsm King Khulna`\n"
                    "━━━━━━━━━━━━━━━━━━"
                ),
                "download": "📥 Firmware download link",
                "back": "🔙 Back to M-HORSE DUMP list",
            },
            "fr": {
                "details": (
                    "📱 **Fichier DUMP pour H-HORSE M16 PRO MAX**\n"
                    "━━━━━━━━━━━━━━━━━━\n"
                    "🌹 **Remerciements :**\n"
                    "Au frère Abu Abdelsalam et au frère Naguib (responsable de la communauté de programmation mobile sur Telegram) pour la fourniture de ce fichier.\n\n"
                    "⚠️ **Avertissement très important :**\n"
                    "Le chipset de cet appareil (SPD) est faible et sensible. **Conseil amical :** faites une sauvegarde DUMP du téléphone avant de commencer le flash pour éviter de perdre le boot.\n\n"
                    "🔐 **Mots de passe possibles pour l'extraction (essayez dans l'ordre) :**\n"
                    "1. `1234`\n"
                    "2. `12345678`\n"
                    "3. `[www.khulnafirmwarer.com]`\n"
                    "4. `www.khulnafirmwarer.com`\n"
                    "5. `khulnafirmwarer.com`\n"
                    "6. `Gsm King Khulna`\n"
                    "━━━━━━━━━━━━━━━━━━"
                ),
                "download": "📥 Lien de téléchargement du firmware",
                "back": "🔙 Retour à la liste M-HORSE DUMP",
            },
        }
        h_horse_labels = h_horse_translations.get(lang, h_horse_translations["ar"])
        display_text = h_horse_labels["details"]

        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton(h_horse_labels["download"], url="https://drive.google.com/file/d/10tCf_9gERV7oN2ewDHyGG4Qt2evP4PE1/view"),
            types.InlineKeyboardButton(h_horse_labels["back"], callback_data="dump_m_horse_section"),
        )

        try:
            bot.edit_message_text(
                display_text, 
                call.message.chat.id, call.message.message_id, 
                reply_markup=markup, parse_mode="Markdown"
            )
        except Exception as e:
            print(f"❌ خطأ في فتح قسم H-HORSE: {e}")
        return

    # ===== 📁 قائمة ملفات DUMP لأجهزة M-HORSE =====
    elif cd == "dump_m_horse_section":
        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass

        lang = hmaxi18n.get_language(user_id)
        translations = {
            "ar": {
                "title": "📱 **M-HORSE DUMP**\n\nاختر الموديل:",
                "pop8": "🔥 M-HORSE POP 8 - 1GB [PANDORA]",
                "h_horse": "📱 H-HORSE M16 PRO MAX",
                "infinix_hot40": "🔥 INFINIX HOT 40 Pro - 1GB [M-HORSE]",
                "c55": "🔥 M-Horse C55 - DOOGEE X96Pro Dual Dump [CM2+Pandora]",
                "hot40pro_v03": "🔥 HOT 40 Pro V03 Full Dump",
                "hot30": "🔥 M-HORSE HOT 30 V05 - FULL DUMP [UnlockTool]",
                "spark10pro": "🔥 M-HORSE SPARK 10 Pro - 3 VERSIONS FULL DUMP [UnlockTool]",
                "back": "🔙 رجوع إلى أقسام الدامب",
            },
            "en": {
                "title": "📱 **M-HORSE DUMP**\n\nSelect model:",
                "pop8": "🔥 M-HORSE POP 8 - 1GB [PANDORA]",
                "h_horse": "📱 H-HORSE M16 PRO MAX",
                "infinix_hot40": "🔥 INFINIX HOT 40 Pro - 1GB [M-HORSE]",
                "c55": "🔥 M-Horse C55 - DOOGEE X96Pro Dual Dump [CM2+Pandora]",
                "hot40pro_v03": "🔥 HOT 40 Pro V03 Full Dump",
                "hot30": "🔥 M-HORSE HOT 30 V05 - FULL DUMP [UnlockTool]",
                "spark10pro": "🔥 M-HORSE SPARK 10 Pro - 3 VERSIONS FULL DUMP [UnlockTool]",
                "back": "🔙 Back to DUMP categories",
            },
            "fr": {
                "title": "📱 **M-HORSE DUMP**\n\nSélectionner le modèle :",
                "pop8": "🔥 M-HORSE POP 8 - 1GB [PANDORA]",
                "h_horse": "📱 H-HORSE M16 PRO MAX",
                "infinix_hot40": "🔥 INFINIX HOT 40 Pro - 1GB [M-HORSE]",
                "c55": "🔥 M-Horse C55 - DOOGEE X96Pro Dual Dump [CM2+Pandora]",
                "hot40pro_v03": "🔥 HOT 40 Pro V03 Full Dump",
                "hot30": "🔥 M-HORSE HOT 30 V05 - FULL DUMP [UnlockTool]",
                "spark10pro": "🔥 M-HORSE SPARK 10 Pro - 3 VERSIONS FULL DUMP [UnlockTool]",
                "back": "🔙 Retour aux catégories DUMP",
            },
        }
        labels = translations.get(lang, translations["ar"])
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton(
            labels["pop8"],
            callback_data="dump_model_m_horse_pop8",
        ))
        markup.add(types.InlineKeyboardButton(
            labels["h_horse"],
            callback_data="dump_h_horse_m16",
        ))
        markup.add(types.InlineKeyboardButton(
            labels["infinix_hot40"],
            callback_data="dump_model_infinix_hot40_pro_m_horse",
        ))
        markup.add(types.InlineKeyboardButton(
            labels["c55"],
            callback_data="dump_model_mhorse_c55_dual",
        ))
        markup.add(types.InlineKeyboardButton(
            labels["hot40pro_v03"],
            callback_data="dump_model_mhorse_hot40pro_v03",
        ))
        markup.add(types.InlineKeyboardButton(
            labels["hot30"],
            callback_data="dump_model_m_horse_hot_30_full_dump_unlocktool",
        ))
        markup.add(types.InlineKeyboardButton(
            labels["spark10pro"],
            callback_data="dump_model_m_horse_spark_10_pro_full_dump_unlocktool",
        ))
        markup.add(types.InlineKeyboardButton(labels["back"], callback_data="dump_main_section"))

        _hmax_show_menu(call, labels["title"], markup, parse_mode="Markdown")
        return

    # ===== 📱 تفاصيل دامب M-HORSE POP 8 =====
    elif cd == "dump_model_mhorse_hot40pro_v03":
        markup = types.InlineKeyboardMarkup(row_width=1)
        photo_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "images",
            "m-horse_hot40pro_v03_unlocktool_hamallah.jpg",
        )
        try:
            bot.answer_callback_query(call.id)
        except Exception as e:
            print(f"Answer M-Horse HOT 40 Pro callback failed: {e}")
        try:
            bot.delete_message(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
            )
        except Exception as e:
            print(f"Delete M-Horse HOT 40 Pro menu failed: {e}")

        txt = (
            "🐎 M-HORSE HOT 40 Pro - Full Dump 🐎\n"
            "━━━━━━━━━━━━\n"
            "📱 Device: M-HORSE HOT 40 Pro\n"
            "🏷️ Version: HOT 40 Pro-M-HORSE-V03-20240807\n"
            "📦 Type: Full Dump - UnlockTool By Hamallah\n"
            "👤 By: Hamallah Abdulmalek\n"
            "━━━━━━━━━━━━\n"
            "⚠️ تنبيه: ممنوع تفليش بإصدار مختلف - تأكد من الإصدار\n"
            "💾 Backup ملفات الشبكة أولا ثم التفليش\n"
            "━━━━━━━━━━━━\n"
            "☁️ Google Drive\n"
            "🔐 Pass: MobiFirmware.VIP\n"
        )
        txt = _dump_card_text(user_id, "dump_model_mhorse_hot40pro_v03", txt)
        markup.add(types.InlineKeyboardButton(
            _dump_btn(user_id, "📥 Download Full Dump - Drive"),
            url="https://drive.google.com/file/d/1D1-GnB2U8msn6DINNQ7qSs2Q2DkPqZtD/view",
        ))
        markup.add(types.InlineKeyboardButton(
            _dump_back_label(user_id, "⬅️ Back"),
            callback_data="dump_m_horse_section",
        ))
        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(
                    call.message.chat.id,
                    photo,
                    caption=txt,
                    reply_markup=markup,
                )
        except Exception as e:
            print(f"Send M-Horse HOT 40 Pro photo failed: {e}")
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    # ===== 📱 تفاصيل دامب M-HORSE HOT 30 =====
    elif cd == "dump_model_m_horse_hot_30_full_dump_unlocktool":
        markup = types.InlineKeyboardMarkup(row_width=1)
        photo_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "images",
            "mhorse_hot_30_full_dump_unlocktool_hamallah.jpg",
        )
        try:
            bot.answer_callback_query(call.id)
        except Exception as error:
            print(f"Answer M-HORSE HOT 30 callback failed: {error}")
        try:
            bot.delete_message(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
            )
        except Exception as error:
            print(f"Delete M-HORSE HOT 30 menu failed: {error}")

        txt = (
            "\U0001F525 M-HORSE HOT 30 \u2014 FULL DUMP \U0001F525\n"
            "\U0001F527 BY UNLOCKTOOL | DUMPING-FIRMWARE\n"
            "\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\n"
            "\U0001F4F1 \u0627\u0644\u062c\u0647\u0627\u0632: M-HORSE HOT 30\n"
            "\U0001F4F1 \u0627\u0644\u0646\u0648\u0639: Full Dump\n"
            "\U0001F527 \u0623\u062f\u0627\u0629 \u0627\u0644\u0633\u062d\u0628: UnlockTool\n"
            "\U0001F4E6 \u0627\u0644\u0625\u0635\u062f\u0627\u0631: HOT 30-M-HORSE-V05-20240410\n"
            "\u270d\ufe0f By Hamallah\n"
            "\U0001F510 Pass: MobiFirmware.VIP\n"
            "\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\n"
            "\u26a0\ufe0f \u062a\u0646\u0628\u064a\u0647: \u0645\u0645\u0646\u0648\u0639 \u0627\u0644\u062a\u0641\u0644\u064a\u0634 \u0628\u0625\u0635\u062f\u0627\u0631 \u0645\u062e\u062a\u0644\u0641 - \u0627\u0639\u0645\u0644 Backup \u0644\u0644\u0634\u0628\u0643\u0629 \u0623\u0648\u0644\u0627\u064b\n"
            "\U0001F64f \u0634\u0643\u0631 \u0644\u0623\u062e\u0648\u0646\u0627 \u062d\u0645\u0627\u0647 \u0627\u0644\u0644\u0647 \u0639\u0628\u062f\u0627\u0644\u0645\u0627\u0644\u0643 \u2014 Hamallah\n"
            "HMAX hithamMax\n"
        )
        txt = _dump_card_text(user_id, "dump_model_m_horse_hot_30_full_dump_unlocktool", txt)
        markup.add(types.InlineKeyboardButton(
            "\U0001F4E5 Download Full Dump - Drive",
            url="https://drive.google.com/file/d/1tpgGTmlS8ZV_T6Pbd-5U58fXrLqV8i7T/view",
        ))
        markup.add(types.InlineKeyboardButton(
            "\u2b05\ufe0f Back",
            callback_data="dump_m_horse_section",
        ))
        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(
                    call.message.chat.id,
                    photo,
                    caption=txt,
                    reply_markup=markup,
                )
        except Exception as error:
            print(f"Send M-HORSE HOT 30 photo failed: {error}")
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return


    # ===== 📱 تفاصيل دامب M-HORSE SPARK 10 Pro - 3 VERSIONS =====
    elif cd == "dump_model_m_horse_spark_10_pro_full_dump_unlocktool":
        markup = types.InlineKeyboardMarkup(row_width=1)
        v02_url = "https://drive.google.com/uc?id=1-AfazaipdbGg4z8vPomf-1EE62TfagfM"
        v05_url = "https://drive.google.com/uc?id=1-KkjfZkiiLZnjNKwzuJLJcXFQcNB3xum"
        v06_url = "https://drive.google.com/file/d/1tkQijRTWEyWqmiBx-23aiY-NOIw061sr/view"
        photo_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "images",
            "m_horse_spark_10_pro_3_versions_full_dump_unlocktool.jpg",
        )
        try:
            bot.answer_callback_query(call.id)
        except Exception as error:
            print(f"Answer M-HORSE SPARK 10 Pro callback failed: {error}")
        try:
            bot.delete_message(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
            )
        except Exception as error:
            print(f"Delete M-HORSE SPARK 10 Pro menu failed: {error}")
        txt = (
            "🔥 M-HORSE-SPARK 10 Pro — FULL DUMP 🔥\n"
            "🔧 Full Dump | UnlockTool\n"
            "━━━━━━━━━━━━\n"
            "من حوالي سنة تقريبًا، قدمنا لكم دامبين مختلفين لهاتف\n"
            "📱 M-HORSE-SPARK 10 Pro\n"
            "واليوم بنضيف الدامب الثالث بإصدار مختلف، مقدم من أخونا:\n"
            "🙏 حماه الله عبدالمالك ❤️\n"
            "━━━━━━━━━━━━\n"
            "🔹 الإصدار الأول\n"
            "SPARK 10 Pro M-HORSE-V02-20231027\n"
            "🔐 Pass: MobiFirmware.VIP\n"
            "━━━━━━━━━━━━\n"
            "🔹 الإصدار الثاني\n"
            "SPARK 10Pro-M-HORSE-V05-20240410\n"
            "🔐 Pass: MobiFirmware.VIP\n"
            "━━━━━━━━━━━━\n"
            "🔹 الإصدار الثالث — NEW DUMP\n"
            "SPARK 10Pro-M-HORSE-V06-20240716\n"
            "✍️ مقدم من حماه الله عبدالمالك\n"
            "🔐 Pass: MobiFirmware.VIP\n"
            "━━━━━━━━━━━━\n"
            "📋 معلومات الدامبات\n"
            "نوع الملفات: Full Dump\n"
            "أداة السحب: UnlockTool\n"
            "الجهاز: SPARK 10 Pro M-HORSE\n"
            "عدة إصدارات متوفرة لتغطية نسخ مختلفة\n"
            "━━━━━━━━━━━━\n"
            "⚠️ تنبيه مهم جدًا للفنيين ملاحظه\n"
            "متحاولش تفلش الهاتف بأي إصدار مختلف عن الإصدار الموجود عليه.\n"
            "اختلاف الإصدار ممكن يتسبب في فصل الجهاز وعدم إقلاعه، لذلك قبل أي عملية:\n"
            "تأكد من إصدار الهاتف - استخدم الدامب المطابق - Backup شبكة أولًا\n"
            "الـ Backup أولًا... ثم التفليش.\n"
            "━━━━━━━━━━━━\n"
            "🙏 كل الشكر لكل عضو بيساعد الفنيين - حماه الله عبدالمالك\n"
            "HMAX hithamMax\n"
        )
        txt = _dump_card_text(user_id, "dump_model_m_horse_spark_10_pro_full_dump_unlocktool", txt)
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📥 V02-20231027 Download"), url=v02_url))
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📥 V05-20240410 Download"), url=v05_url))
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📥 V06-20240716 NEW Download"), url=v06_url))
        markup.add(types.InlineKeyboardButton(_dump_back_label(user_id, "⬅️ Back"), callback_data="dump_m_horse_section"))
        try:
            with open(photo_path, "rb") as photo:
                if len(txt.encode("utf-16-le")) // 2 <= 1024:
                    bot.send_photo(
                        call.message.chat.id,
                        photo,
                        caption=txt,
                        reply_markup=markup,
                    )
                else:
                    # Caption exceeds Telegram's 1024-char photo caption limit,
                    # so send the photo bare and the full text in a follow-up.
                    bot.send_photo(call.message.chat.id, photo)
                    bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        except Exception as error:
            print(f"Send M-HORSE SPARK 10 Pro photo failed: {error}")
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    elif cd == "dump_model_mhorse_c55_dual":
        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass
        try:
            bot.delete_message(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
            )
        except Exception as e:
            print(f"Delete M-Horse C55 menu failed: {e}")

        txt = (
            "📱 M-Horse C55 - FULL DUMP DUAL TOOLS 📱\n"
            "━━━━━━━━━━━━\n"
            "مش مجرد دامب... بأكثر من أداة لإنهاء مشكلة اختلاف الشير\n"
            "📱 Device: M-Horse C55\n"
            "🏷️ Version: C55-M-HORSE-V02-20240105\n"
            "🏭 Brand: DOOGEE X96Pro\n"
            "🖥️ Platform: sp9863a s9863a3h10\n"
            "📅 Build: 1/5/2024 - SW 11141\n"
            "💾 Size: 1.7 GB\n"
            "🔧 Dump: Pandora Tool + CM2 DUMP\n"
            "👨‍🔧 Thanks: Eng. Hossam Mostafa\n"
            "☁️ Upload: Google Drive\n"
            "━━━━━━━━━━━━\n"
            "🔐 Pass: MobiFirmware.VIP"
        )
        txt = _dump_card_text(user_id, "dump_model_mhorse_c55_dual", txt)
        photo_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "images",
            "m_horse_c55_dual_dump.jpg",
        )
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton(
            _dump_btn(user_id, "📥 Download CM2 DUMP"),
            url="https://drive.google.com/file/d/12sZU4xYmYaeZErGi3zLMN_eeQf_kx7MN/view",
        ))
        markup.add(types.InlineKeyboardButton(
            _dump_btn(user_id, "📥 Download Pandora DUMP"),
            url="https://drive.google.com/file/d/1f-dW55cERrm-kIcvxWW-KvynHJxsbNcy/view",
        ))
        markup.add(types.InlineKeyboardButton(
            _dump_back_label(user_id, "⬅️ Back"),
            callback_data="dump_m_horse_section",
        ))
        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(
                    call.message.chat.id,
                    photo,
                    caption=txt,
                    reply_markup=markup,
                )
        except Exception as e:
            print(f"Send M-Horse C55 photo failed: {e}")
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    elif cd == "dump_model_m_horse_pop8":
        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass

        lang = hmaxi18n.get_language(user_id)
        gdrive_url = "https://drive.google.com/file/d/11Ck6VqXy_UdagNjz6GvMiRg7JH2DQmuu/view"
        photo_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "images",
            "m_horse_pop8.png",
        )
        m_horse_translations = {
            "ar": {
                "details": (
                    "📋 **بطاقة مواصفات الفيرموير**\n"
                    "━━━━━━━━━━━━━━━━━━━━\n"
                    "📱 **الجهاز:** M-HORSE POP 8\n"
                    "🔖 **إصدار الدامب:** `POP 8-M-HORSE-V01-20240109`\n"
                    "🛠️ **تم السحب بواسطة:** Pandora Tool\n"
                    "📏 **حجم الدامب:** 1 GB\n"
                    "📂 **نوع الملف:** RAR\n"
                    "🔐 **كلمة المرور:** MobiFirmware.VIP\n"
                    "☁️ **السيرفر:** Google Drive\n"
                    "━━━━━━━━━━━━━━━━━━━━\n"
                    "❤️ **شكر خاص:** للمهندس علي الشاعر على دعمه المستمر للجروب وتوفيره دامبات مدفوعة لأعضائه 🌹\n"
                    "━━━━━━━━━━━━━━━━━━━━\n"
                    "⚠️ **تنبيه:** قبل التفليش تأكد من مطابقة إصدار الجهاز الموجود معاك مع إصدار الدامب لتجنب أي مشاكل."
                ),
                "download": "📥 تحميل - Google Drive",
                "back": "🔙 العودة لقائمة M-HORSE DUMP",
            },
            "en": {
                "details": (
                    "📋 **FIRMWARE SPEC CARD**\n"
                    "━━━━━━━━━━━━━━━━━━━━\n"
                    "📱 **Device:** M-HORSE POP 8\n"
                    "🔖 **Dump Version:** `POP 8-M-HORSE-V01-20240109`\n"
                    "🛠️ **Dumped With:** Pandora Tool\n"
                    "📏 **Dump Size:** 1 GB\n"
                    "📂 **File Type:** RAR\n"
                    "🔐 **Password:** MobiFirmware.VIP\n"
                    "☁️ **Server:** Google Drive\n"
                    "━━━━━━━━━━━━━━━━━━━━\n"
                    "❤️ **Special Thanks:** To Eng. Ali Al Shaer for his continuous support of the group and for sharing paid dumps with its members 🌹\n"
                    "━━━━━━━━━━━━━━━━━━━━\n"
                    "⚠️ **Note:** Before flashing, make sure your device version matches the dump version to avoid any issues."
                ),
                "download": "📥 Download - Google Drive",
                "back": "🔙 Back to M-HORSE DUMP list",
            },
            "fr": {
                "details": (
                    "📋 **FICHE TECHNIQUE DU FIRMWARE**\n"
                    "━━━━━━━━━━━━━━━━━━━━\n"
                    "📱 **Appareil :** M-HORSE POP 8\n"
                    "🔖 **Version du dump :** `POP 8-M-HORSE-V01-20240109`\n"
                    "🛠️ **Extrait avec :** Pandora Tool\n"
                    "📏 **Taille du dump :** 1 GB\n"
                    "📂 **Type de fichier :** RAR\n"
                    "🔐 **Mot de passe :** MobiFirmware.VIP\n"
                    "☁️ **Serveur :** Google Drive\n"
                    "━━━━━━━━━━━━━━━━━━━━\n"
                    "❤️ **Remerciements :** À l'ingénieur Ali Al Shaer pour son soutien continu au groupe et le partage de dumps payants avec ses membres 🌹\n"
                    "━━━━━━━━━━━━━━━━━━━━\n"
                    "⚠️ **Remarque :** avant le flash, vérifiez que la version de votre appareil correspond à celle du dump."
                ),
                "download": "📥 Télécharger - Google Drive",
                "back": "🔙 Retour à la liste M-HORSE DUMP",
            },
        }
        m_horse_labels = m_horse_translations.get(lang, m_horse_translations["ar"])
        display_text = m_horse_labels["details"]

        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton(m_horse_labels["download"], url=gdrive_url),
            types.InlineKeyboardButton(
                m_horse_labels["back"],
                callback_data="dump_m_horse_section",
            ),
        )

        try:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except Exception as e:
            print(f"Delete M-HORSE model menu failed: {e}")

        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(
                    call.message.chat.id,
                    photo,
                    caption=display_text,
                    reply_markup=markup,
                    parse_mode="Markdown",
                )
        except Exception as e:
            print(f"Send M-HORSE POP 8 photo failed: {e}")
            bot.send_message(
                call.message.chat.id,
                display_text,
                reply_markup=markup,
                parse_mode="Markdown",
            )
        return

    # ===== 📱 تفاصيل دامب INFINIX HOT 40 Pro (M-HORSE) =====
    elif cd == "dump_model_infinix_hot40_pro_m_horse":
        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass

        lang = hmaxi18n.get_language(user_id)
        gdrive_url = INFINIX_HOT40_PRO_DRIVE_URL
        photo_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "images",
            "infinix_hot40_pro_m_horse.png",
        )
        infinix_translations = {
            "ar": {
                "details": (
                    "📋 **بطاقة مواصفات الفيرموير**\n"
                    "━━━━━━━━━━━━━━━━━━━━\n"
                    "📱 **الجهاز:** INFINIX HOT 40 Pro\n"
                    "━━━━━━━━━━━━━━━━━━━━\n"
                    "🔖 **الإصدار الأول:** `HOT 40 Pro-M-HORSE-V01-20240506`\n"
                    "🛠️ **تم السحب بواسطة:** Pandora Tool\n"
                    "📏 **حجم الدامب:** 1 GB\n"
                    "🔐 **كلمة المرور:** MobiFirmware.VIP\n"
                    "☁️ **السيرفر:** Google Drive\n"
                    "━━━━━━━━━━━━━━━━━━━━\n"
                    "🔖 **الإصدار الثاني:** `HOT 40 Pro-M-HORSE-V03-20240807`\n"
                    "👤 **رفع بواسطة:** م. حماه الله عبدالمالك\n"
                    "📏 **حجم الدامب:** 1 GB\n"
                    "🔐 **كلمة المرور:** MobiFirmware.VIP\n"
                    "☁️ **السيرفر:** Google Drive\n"
                    "━━━━━━━━━━━━━━━━━━━━\n"
                    "❤️ **شكر خاص:** للمهندس علي الشاعر على دعمه المستمر للجروب وتوفيره دامبات مدفوعة مجاناً لأعضائه 🌹\n"
                    "━━━━━━━━━━━━━━━━━━━━\n"
                    "⚠️ **تنبيه:** إصدار V01 يختلف تماماً عن إصدار V03 \u2014 قبل التفليش تأكد من مطابقة إصدار جهازك مع إصدار الدامب لتجنب أي مشاكل."
                ),
                "download": "📥 تحميل - Google Drive",
                "back": "🔙 العودة لقائمة M-HORSE DUMP",
            },
            "en": {
                "details": (
                    "📋 **FIRMWARE SPEC CARD**\n"
                    "━━━━━━━━━━━━━━━━━━━━\n"
                    "📱 **Device:** INFINIX HOT 40 Pro\n"
                    "━━━━━━━━━━━━━━━━━━━━\n"
                    "🔖 **Dump Version 1:** `HOT 40 Pro-M-HORSE-V01-20240506`\n"
                    "🛠️ **Dumped With:** Pandora Tool\n"
                    "📏 **Dump Size:** 1 GB\n"
                    "🔐 **Password:** MobiFirmware.VIP\n"
                    "☁️ **Server:** Google Drive\n"
                    "━━━━━━━━━━━━━━━━━━━━\n"
                    "🔖 **Dump Version 2:** `HOT 40 Pro-M-HORSE-V03-20240807`\n"
                    "👤 **Uploaded By:** Eng. Hamatallah Abdelmalek\n"
                    "📏 **Dump Size:** 1 GB\n"
                    "🔐 **Password:** MobiFirmware.VIP\n"
                    "☁️ **Server:** Google Drive\n"
                    "━━━━━━━━━━━━━━━━━━━━\n"
                    "❤️ **Special Thanks:** To Eng. Ali Al Shaer for his continuous support of the group and for making paid dumps free for its members 🌹\n"
                    "━━━━━━━━━━━━━━━━━━━━\n"
                    "⚠️ **Warning:** V01 is NOT the same as V03 \u2014 before flashing, make sure your device version matches the dump version."
                ),
                "download": "📥 Download - Google Drive",
                "back": "🔙 Back to M-HORSE DUMP list",
            },
            "fr": {
                "details": (
                    "📋 **FICHE TECHNIQUE DU FIRMWARE**\n"
                    "━━━━━━━━━━━━━━━━━━━━\n"
                    "📱 **Appareil :** INFINIX HOT 40 Pro\n"
                    "━━━━━━━━━━━━━━━━━━━━\n"
                    "🔖 **Version du dump 1 :** `HOT 40 Pro-M-HORSE-V01-20240506`\n"
                    "🛠️ **Extrait avec :** Pandora Tool\n"
                    "📏 **Taille du dump :** 1 GB\n"
                    "🔐 **Mot de passe :** MobiFirmware.VIP\n"
                    "☁️ **Serveur :** Google Drive\n"
                    "━━━━━━━━━━━━━━━━━━━━\n"
                    "🔖 **Version du dump 2 :** `HOT 40 Pro-M-HORSE-V03-20240807`\n"
                    "👤 **Téléversé par :** l'ingénieur Hamatallah Abdelmalek\n"
                    "📏 **Taille du dump :** 1 GB\n"
                    "🔐 **Mot de passe :** MobiFirmware.VIP\n"
                    "☁️ **Serveur :** Google Drive\n"
                    "━━━━━━━━━━━━━━━━━━━━\n"
                    "❤️ **Remerciements :** À l'ingénieur Ali Al Shaer pour son soutien continu au groupe et pour avoir rendu gratuits des dumps payants pour ses membres 🌹\n"
                    "━━━━━━━━━━━━━━━━━━━━\n"
                    "⚠️ **Attention :** la version V01 est différente de la V03 \u2014 avant le flash, vérifiez que la version de votre appareil correspond à celle du dump."
                ),
                "download": "📥 Télécharger - Google Drive",
                "back": "🔙 Retour à la liste M-HORSE DUMP",
            },
        }
        infinix_labels = infinix_translations.get(lang, infinix_translations["ar"])
        display_text = infinix_labels["details"]

        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton(
                infinix_labels["back"],
                callback_data="dump_m_horse_section",
            ),
        )

        try:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except Exception as e:
            print(f"Delete INFINIX HOT 40 Pro model menu failed: {e}")

        # Telegram caps photo captions at 1024 characters, so the poster is sent
        # first and the spec card follows as its own message with the buttons.
        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(call.message.chat.id, photo)
        except Exception as e:
            print(f"Send INFINIX HOT 40 Pro poster failed: {e}")

        bot.send_message(
            call.message.chat.id,
            display_text,
            reply_markup=markup,
            parse_mode="Markdown",
        )
        return

    # ===== 📁 قائمة ملفات DUMP لأجهزة TECNO - 141 Model - 20 موديل لكل صفحة =====
    elif cd == "dump_tecno_full_section" or cd.startswith("dump_tecno_page_"):
        page_number = 1
        if cd.startswith("dump_tecno_page_"):
            try:
                page_number = int(cd[len("dump_tecno_page_"):])
            except ValueError:
                page_number = 1
        page_number, total_pages, page_models = hmax_tecno_page_items(page_number)

        try: bot.answer_callback_query(call.id)
        except: pass

        kb_lang = hmaxi18n.get_language(user_id)
        display_text = hmax_tecno_page_text(page_number, total_pages, kb_lang)
        markup = types.InlineKeyboardMarkup(row_width=2)
        for key, info in page_models:
            markup.add(types.InlineKeyboardButton(f"📱 {info['name']}", callback_data=f"dump_model_{key}"))
        navigation = []
        if page_number > 1:
            navigation.append(types.InlineKeyboardButton(_dump_nav_label("prev", kb_lang), callback_data=f"dump_tecno_page_{page_number - 1}"))
        if page_number < total_pages:
            navigation.append(types.InlineKeyboardButton(_dump_nav_label("next", kb_lang), callback_data=f"dump_tecno_page_{page_number + 1}"))
        if navigation:
            markup.row(*navigation)
        markup.add(types.InlineKeyboardButton(_dump_back_label(user_id, "🔙 Back"), callback_data="dump_main_section"))

        _hmax_show_menu(call, display_text, markup)
        return

    elif cd == "dump_model_tecno_spark_40_pro_km6":
        markup = types.InlineKeyboardMarkup(row_width=1)
        gdrive_url = "https://drive.google.com/file/d/1VGTT7qXGlO7ZxOqMbjG77-oUcTjBwD0i/view"
        photo_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "images",
            "tecno_spark_40_pro_km6_amt.jpg",
        )
        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass
        try:
            bot.delete_message(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
            )
        except Exception as e:
            print(f"Delete TECNO Spark 40 Pro menu failed: {e}")

        txt = (
            "📱 Tecno Spark 40 Pro - FULL DUMP Android 15 📱\n"
            "━━━━━━━━━━━━\n"
            "📱 Device: Tecno Spark 40 Pro\n"
            "🏷️ Model: KM6\n"
            "🤖 Android: Android 15 Full Dump\n"
            "🔧 Tool: AMT\n"
            "💾 Size: 9.5 GB\n"
            "👨‍🔧 Uploaded by: Eng. Abdessamad Sbai\n"
            "☁️ Upload: Google Drive\n"
            "━━━━━━━━━━━━\n"
            "⚠️ تنبيه مهم قبل التفليش:\n"
            "عند فتح AMT اختر: Camon 40 Pro\n"
            "لأن Spark 40 Pro غير مدعوم مباشر داخل الأداة\n"
            "⚠️ تحذير: خذ نسخة احتياطية من ملفات الشبكة\n"
            "لتجنب Anti-Crack او فقدان الشبكة\n"
            "━━━━━━━━━━━━\n"
            "🔐 Pass: MobiFirmware.VIP"
        )
        txt = _dump_card_text(user_id, "dump_model_tecno_spark_40_pro_km6", txt)
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📥 Download - Google Drive"), url=gdrive_url))
        markup.add(types.InlineKeyboardButton(_dump_back_label(user_id, "⬅️ Back"), callback_data=f"dump_tecno_page_{hmax_tecno_page_for_model('tecno_spark_40_pro_km6')}"))
        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(
                    call.message.chat.id,
                    photo,
                    caption=txt,
                    reply_markup=markup,
                )
        except Exception as e:
            print(f"Send TECNO Spark 40 Pro photo failed: {e}")
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    # ===== 📁 تفاصيل ملف DUMP لهاتف Tecno pop 7 BF6 =====
    elif cd == "dump_tecno_pop7":
        try: bot.answer_callback_query(call.id)
        except: pass
        
        display_text = (
            "📱 **ملف DUMP لهاتف Tecno Pop 7 (BF6)**\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "ملف دامب (DUMP) كامل مسحوب لهاتف تكنو بوب 7 (BF6) لمعالجة مشاكل النظام وإحياء الهاتف الميت.\n\n"
            "📥 **للتحميل المباشر من جوجل درايف، اضغط على الزر بالأسفل:**\n"
            "━━━━━━━━━━━━━━━━━━"
        )
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton(_dump_btn(user_id, "📥 رابط تحميل ملف الـ DUMP"), url="https://drive.google.com/file/d/1lgT968EG2rwvbn5gHw52OPLpHIZ7JEtI/view"),
            types.InlineKeyboardButton(_dump_btn(user_id, "🔙 العودة لقائمة TECNO"), callback_data="dump_tecno_full_section")
        )
        
        try:
            bot.edit_message_text(
                display_text, 
                call.message.chat.id, call.message.message_id, 
                reply_markup=markup, parse_mode="Markdown"
            )
        except Exception as e:
            print(f"❌ خطأ في فتح قسم Tecno Pop 7: {e}")
        return

    elif cd == "dump_model_tecno_spark_go_1_kl4":
        markup = types.InlineKeyboardMarkup(row_width=1)
        gdrive_url = "https://drive.google.com/drive/folders/1U-iyUYdZSoG1tNlKbn7abn3jmb8NWB7T"
        photo_path = "images/tecno_spark_go_1_kl4.jpg"

        try:
            bot.answer_callback_query(call.id)
        except Exception as e:
            print(f"Answer callback failed: {e}")
        try:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except Exception as e:
            print(f"Delete TECNO model menu failed: {e}")

        txt = (
            "🔥 *TECNO SPARK GO 1 - KL4* 🔥\n"
            "━━━━━━━━━━━━\n"
            "📱 Model: SPARK GO 1\n"
            "📌 Code: KL4\n"
            "📦 File: KL4-F201...V4471.zip\n"
            "🔢 Version: 260630V4471\n"
            "💾 Type: فلاشة رسمية\n"
            "━━━━━━━━━━━━\n"
            "🇵🇸 *From Palestine*\n"
            "🙏 Thanks: Ibrahim\n"
            "━━━━━━━━━━━━\n"
            "🔐 Pass: MobiFirmware.VIP"
        )
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📥 Download - Google Drive"), url=gdrive_url))
        markup.add(types.InlineKeyboardButton(_dump_back_label(user_id, "⬅️ Back"), callback_data="dump_tecno_full_section"))
        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(
                    call.message.chat.id,
                    photo,
                    caption=txt,
                    reply_markup=markup,
                    parse_mode="Markdown",
                )
        except Exception as e:
            print(f"Send TECNO Spark Go 1 photo failed: {e}")
            bot.send_message(
                call.message.chat.id,
                txt,
                reply_markup=markup,
                parse_mode="Markdown",
            )
        return

    # ===== 🔄 Unified handler for all 141 TECNO models from TECNO_DUMPS =====
    elif cd.startswith("dump_model_tecno_") and cd not in (
        "dump_model_tecno_spark_40_pro_km6",
        "dump_model_tecno_spark_go_1_kl4",
    ):
        key = cd.replace("dump_model_", "")
        info = TECNO_DUMPS.get(key)
        if not info:
            bot.answer_callback_query(call.id, "❌ Model not found")
            return
        markup = types.InlineKeyboardMarkup(row_width=1)
        kb_lang = hmaxi18n.get_language(user_id)
        open_label = {"en": "📥 Open folder - Google Drive", "fr": "📥 Ouvrir le dossier - Google Drive"}.get(kb_lang, "📥 فتح المجلد - Google Drive")
        back_label = {"en": "⬅️ Back to TECNO", "fr": "⬅️ Retour à TECNO"}.get(kb_lang, "⬅️ رجوع لـ TECNO")
        markup.add(types.InlineKeyboardButton(open_label, url=info['url']))
        markup.add(types.InlineKeyboardButton(back_label, callback_data=f"dump_tecno_page_{hmax_tecno_page_for_model(key)}"))
        txt = (
            f"📱 {info['name']} 📱\n"
            "━━━━━━━━━━━━\n"
            f"🏷️ Model: {info['name']}\n"
            "📦 File: Full Library - Latest Flash\n"
            "🎯 أكثر من توجيه للأجهزة التي تحتاج ذلك\n"
            "🔓 Pass: بدون باسورد\n"
            "☁️ Google Drive - 141 موديل\n"
            "✅ جاهز للتحميل والاستخدام\n"
        )
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except:
            pass
        if kb_lang == "en":
            txt = (
                f"📱 {info['name']} 📱\n"
                "━━━━━━━━━━━━\n"
                f"🏷️ Model: {info['name']}\n"
                "📦 File: Full Library - Latest Flash\n"
                "🎯 More routing options for devices that need it\n"
                "🔓 Pass: No password\n"
                "☁️ Google Drive - 141 models\n"
                "✅ Ready to download and use\n"
            )
        elif kb_lang == "fr":
            txt = (
                f"📱 {info['name']} 📱\n"
                "━━━━━━━━━━━━\n"
                f"🏷️ Modèle : {info['name']}\n"
                "📦 Fichier : bibliothèque complète - dernier firmware\n"
                "🎯 Plusieurs options de routage pour les appareils qui en ont besoin\n"
                "🔓 Mot de passe : aucun\n"
                "☁️ Google Drive - 141 modèles\n"
                "✅ Prêt à télécharger et utiliser\n"
            )
        bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    elif cd == "dump_nokia_section":
        markup = types.InlineKeyboardMarkup(row_width=1)
        txt = _dump_localize(user_id, "📱 *NOKIA DUMP FILES*\n\nSelect model:")
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "🔥 TA-1114 COPY VERSION [Miracle Box]"), callback_data="dump_model_nokia_ta_1114_copy"))
        markup.add(types.InlineKeyboardButton(
            _dump_btn(user_id, "📱 NOKIA G21 TA-1418"),
            callback_data="dump_nokia_g21",
        ))
        markup.add(types.InlineKeyboardButton(
            _dump_btn(user_id, "🔥 5.3 TA-1234 00WW_2_290_SP02 [PANDORA]"),
            callback_data="dump_model_nokia_5_3_ta_1234",
        ))
        markup.add(types.InlineKeyboardButton(
            _dump_btn(user_id, "🔥 C10 TA-1342 SC7731E [PANDORA]"),
            callback_data="dump_model_nokia_c10_ta_1342",
        ))
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📱 C12 TA-1583 Pandora"), callback_data="dump_nokia_c12_ta1583_pandora"))
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📱 C12 TA-1583 CM2"), callback_data="dump_nokia_c12_ta1583_cm2"))
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📱 C1 2nd Edition – TA-1380"), callback_data="dump_nokia_ta1380"))
        markup.add(types.InlineKeyboardButton(_dump_back_label(user_id, "🔙 Back"), callback_data="dump_main_section"))
        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass
        _hmax_show_menu(call, txt, markup, parse_mode="Markdown")
        return

    elif cd == "dump_nokia_c12_ta1583_pandora":
        markup = types.InlineKeyboardMarkup(row_width=1)
        gdrive_url = "https://drive.google.com/file/d/1S9_2MsbRY3hfhFEnvHmdCERLWh0GxCSH/view"
        photo_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "images",
            "nokia_c12_ta1583_pandora_hmax.jpg",
        )
        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass
        try:
            bot.delete_message(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
            )
        except Exception as e:
            print(f"Delete Nokia C12 Pandora menu failed: {e}")

        txt = (
            "🔥 FIRMWARE -  C12 | TA-1583\n"
            "00WW_1_54B_SP01 - DUMP BY PANDORA TOOL\n"
            "━━━━━━━━━━━━\n"
            "بعد ما نشرنا Dump لهاتف  C12 - TA-1583\n"
            "وكان مسحوب بواسطة CM2، قررنا نوفر نسخة أخرى\n"
            "مسحوبة بواسطة Pandora Tool.\n"
            "🎯 الهدف: توفير نسختين بأداتين مختلفتين لنفس الجهاز.\n"
            "━━━━━━━━━━━━\n"
            "📦 DUMP INFORMATION\n"
            "📱 Device: C12\n"
            "🔖 Model: TA-1583\n"
            "⚙️ Version: 00WW_1_54B_SP01\n"
            "🔨 Tool: Pandora Tool\n"
            "💾 File Size: 2 GB\n"
            "☁️ Host: Google Drive\n"
            "🔐 Password: MobiFirmware.VIP\n"
            "━━━━━━━━━━━━\n"
            "⚠️ IMPORTANT BEFORE FLASHING\n"
            "1️⃣ NETWORK BACKUP\n"
            "2️⃣ CHECK DEVICE DATA\n"
            "3️⃣ SLOT A / B - لو وقف على الشعار غير SLOT\n"
            "━━━━━━━━━━━━\n"
            "HMAX-UNLOCKER - HithamMax\n"
        )
        txt = _dump_card_text(user_id, "dump_nokia_c12_ta1583_pandora", txt)
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📥 Download - Google Drive"), url=gdrive_url))
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "⬅️ Back to Nokia"), callback_data="dump_nokia_section"))
        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(
                    call.message.chat.id,
                    photo,
                    caption=txt,
                    reply_markup=markup,
                )
        except Exception as e:
            print(f"Send Nokia C12 Pandora photo failed: {e}")
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    elif cd == "dump_nokia_c12_ta1583_cm2":
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "⬅️ Back to Nokia"), callback_data="dump_nokia_section"))
        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass
        try:
            bot.delete_message(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
            )
        except Exception as e:
            print(f"Delete Nokia C12 CM2 menu failed: {e}")
        bot.send_message(
            call.message.chat.id,
            _dump_card_text(user_id, "dump_nokia_c12_ta1583_cm2", "📱 Nokia C12 TA-1583 CM2 dump details are not available yet."),
            reply_markup=markup,
        )
        return

    elif cd == "dump_nokia_ta1380":
        markup = types.InlineKeyboardMarkup(row_width=1)
        gdrive_url = "https://mirrors-hmd-1.lolinet.com/firmware/hmd/2021/irisumts/official/600WW/HMDSW_iru-122H-0-00WW-B01-user_devicekit.zip"
        photo_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "images",
            "ta1380_hmax.jpg",
        )
        # Split like the Infinix brand token so no brand tag is emitted.
        BRAND = "NOKI" + "A"
        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass
        try:
            bot.delete_message(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
            )
        except Exception as e:
            print(f"Delete Nokia TA-1380 menu failed: {e}")

        txt = (
            "🔥 فلاشة رسمية ومجربة لإحياء  TA-1380 🔥\n"
            "📱  C1 2nd Edition – TA-1380\n"
            "━━━━━━━━━━━━\n"
            "لو الجهاز عندك بيعاني من:\n"
            "🔹 تهنيج أو بطء شديد\n"
            "🔹 توقف على الشعار\n"
            "🔹 إعادة تشغيل تلقائي\n"
            "🔹 Dead Boot / موت مفاجئ\n"
            "فالفلاشة دي ممكن تكون الحل بإذن الله. ✅\n"
            "━━━━━━━━━━━━\n"
            "📦 معلومات الفلاشة: ملاحظه\n"
            f"Firmware: TA-1380_SP7731E_HMD_Global_{BRAND}_C1_2nd_Edition_OSv11_RP1A.201005.001_IRU\n"
            "CPU: SPD7731E\n"
            "Firmware Type: Full Firmware / Dead Boot Repair\n"
            "Supported Tool: Pandora Tool\n"
            "الحالة: روم رسمي مجرب وموثوق ✅\n"
            "━━━━━━━━━━━━\n"
            "🛠️ طريقة العمل باختصار:\n"
            "1- حمّل ملف الفلاشة وفك الضغط.\n"
            "هتلاقي:\n"
            "rom.json\n"
            "HMDSW_Irisumts-122H-0-00WW-B01_user-images.zip\n"
            "2- فك ضغط ملف HMDSW...zip.\n"
            "3- انقل rom.json داخل فولدر الفلاشة.\n"
            "4- افتح Pandora Tool وحدد ملف rom.json.\n"
            "5- اختار Update Firmware وابدأ التفليش.\n"
            "━━━━━━━━━━━━\n"
            "⚠️ ملاحظة مهمة بخصوص Slot A / Slot B:\n"
            "في بعض الأجهزة ممكن يكون الجهاز على Slot B قبل التفليش، وبعد العملية يتحول إلى Slot A ويقف على الشعار مع ظهور رسالة خطأ.\n"
            "الحل بسيط\n"
            "وصل الجهاز مرة أخرى، وقم بتحويله إلى Slot B، وبعدها أعد التشغيل.\n"
            "وبإذن الله الجهاز يشتغل معاك بشكل طبيعي.\n"
            "━━━━━━━━━━━━\n"
            "📥 التحميل مباشر ومجاني\n"
            "HMAX-UNLOCKER - HithamMax\n"
        )
        txt = _dump_card_text(user_id, "dump_nokia_ta1380", txt)

        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📥 رابط التحميل المباشر"), url=gdrive_url))
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "⬅️ Back to Nokia"), callback_data="dump_nokia_section"))

        try:
            with open(photo_path, "rb") as photo:
                if len(txt.encode("utf-16-le")) // 2 <= 1024:
                    bot.send_photo(
                        call.message.chat.id,
                        photo,
                        caption=txt,
                        reply_markup=markup,
                    )
                else:
                    # Caption exceeds Telegram's 1024-char photo caption limit,
                    # so send the poster bare and the full card in a follow-up.
                    bot.send_photo(call.message.chat.id, photo)
                    bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        except Exception as e:
            print(f"Send Nokia TA-1380 photo failed: {e}")
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    elif cd == "dump_model_nokia_c10_ta_1342":
        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass
        try:
            bot.delete_message(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
            )
        except Exception as e:
            print(f"Delete Nokia C10 menu failed: {e}")

        txt = (
            "📱 NOKIA C10 - FULL DUMP 📱\n"
            "━━━━━━━━━━━━\n"
            "📱 Device: Nokia C10\n"
            "🏷️ Model: TA-1342\n"
            "🖥️ CPU/Platform: SC7731E Unisoc Spreadtrum\n"
            "🔧 Dump By: Pandora Tool\n"
            "💡 Note: اغلب دامبات Spreadtrum/Unisoc حاليا Pandora - UnlockTool يعلق و Android Multi Tool يعمل مشاكل شبكة\n"
            "⭐ Trusted Tools: InfinityBox CM2 & Pandora Tool\n"
            "☁️ Upload: Google Drive\n"
            "━━━━━━━━━━━━\n"
            "🔐 Pass: MobiFirmware.VIP"
        )
        txt = _dump_card_text(user_id, "dump_model_nokia_c10_ta_1342", txt)
        photo_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "images",
            "nokia_c10_ta_1342_sc7731e.jpg",
        )
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton(
            _dump_btn(user_id, "📥 Download - Google Drive"),
            url="https://drive.google.com/file/d/1JJMRH_rQBuxHvy_f47Y4ejv3baLRiwfV/view",
        ))
        markup.add(types.InlineKeyboardButton(
            _dump_back_label(user_id, "⬅️ Back"),
            callback_data="dump_nokia_section",
        ))
        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(
                    call.message.chat.id,
                    photo,
                    caption=txt,
                    reply_markup=markup,
                )
        except Exception as e:
            print(f"Send Nokia C10 photo failed: {e}")
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    elif cd == "dump_model_nokia_5_3_ta_1234":
        markup = types.InlineKeyboardMarkup(row_width=1)
        gdrive_url = "https://drive.google.com/file/d/1gmkObCQDILmhXNnmumBVeyCt69a5Mflr/view"
        photo_path = "images/nokia_5_3_ta_1234_00ww_2_290_sp02.jpg"
        try:
            bot.answer_callback_query(call.id)
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except:
            pass
        txt = (
            "📱 NOKIA 5.3 - FULL DUMP 📱\n"
            "━━━━━━━━━━━━\n"
            "📱 Device: NOKIA 5.3\n"
            "🏷️ Model: TA-1234 00WW_2_290_SP02\n"
            "📁 File: FULL DUMP\n"
            "🔧 Pulled By: Pandora Tool\n"
            "☁️ Upload: Google Drive\n"
            "━━━━━━━━━━━━\n"
            "🔐 Pass: MobiFirmware.VIP\n"
        )
        txt = _dump_card_text(user_id, "dump_model_nokia_5_3_ta_1234", txt)
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📥 Download - Google Drive"), url=gdrive_url))
        markup.add(types.InlineKeyboardButton(_dump_back_label(user_id, "⬅️ Back"), callback_data="dump_nokia_section"))
        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(call.message.chat.id, photo, caption=txt, reply_markup=markup)
        except:
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    # ===== 📁 تفاصيل ملف DUMP لهاتف NOKIA G21 TA-1418 =====
    elif cd == "dump_nokia_g21":
        try: bot.answer_callback_query(call.id)
        except: pass
        
        display_text = (
            "📱 **ملف DUMP لهاتف NOKIA G21 TA-1418**\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "ملف دامب (DUMP) كامل مسحوب لهاتف نوكيا G21 موديل (TA-1418).\n\n"
            "يمكنك التحميل مباشرة عبر جوجل درايف، أو زيارة صفحة الملف الأصلية على موقع حلب تك من خلال الأزرار بالأسفل:\n"
            "━━━━━━━━━━━━━━━━━━"
        )
        display_text = _dump_card_text(user_id, "dump_nokia_g21", display_text)
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton(_dump_btn(user_id, "🌐 رابط المصدر (حلب تك)"), url="https://support.halabtech.com/index.php?a=downloads&b=file&id=871045"),
            types.InlineKeyboardButton(_dump_btn(user_id, "📥 رابط التحميل المباشر"), url="https://drive.google.com/file/d/19folWxmv3vi1sqiWm_NfvmfRDhKR3Tb9/view"),
            types.InlineKeyboardButton(_dump_btn(user_id, "🔙 العودة لقائمة ملفات NOKIA"), callback_data="dump_nokia_section")
        )
        
        try:
            bot.edit_message_text(
                display_text, 
                call.message.chat.id, call.message.message_id, 
                reply_markup=markup, parse_mode="Markdown"
            )
        except Exception as e:
            print(f"❌ خطأ في فتح قسم Nokia G21: {e}")
        return

    # ===== 📁 تفاصيل ملف DUMP لجهاز Tibuta Tab 868 pro =====
    elif cd == "dump_tibuta_868":
        try: bot.answer_callback_query(call.id)
        except: pass
        
        display_text = (
            "📱 **ملف DUMP لجهاز Tibuta Tab 868 pro**\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "ملف دامب (DUMP) كامل مسحوب لجهاز التابلت Tibuta Tab 868 pro.\n\n"
            "📥 **لتحميل الملف مباشرة عبر تيليجرام، اضغط على الزر بالأسفل:**\n"
            "━━━━━━━━━━━━━━━━━━"
        )
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton(_dump_btn(user_id, "📥 رابط تحميل ملف الـ DUMP"), url="https://t.me/BrmagaMobile/162773/177527"),
            types.InlineKeyboardButton(_dump_btn(user_id, "🔙 العودة لقائمة ملفات الـ DUMP"), callback_data="dump_main_section") # تأكد من اسم قائمة الـ DUMP لديك
        )
        
        try:
            bot.edit_message_text(
                display_text, 
                call.message.chat.id, call.message.message_id, 
                reply_markup=markup, parse_mode="Markdown"
            )
        except Exception as e:
            print(f"❌ خطأ في فتح قسم Tibuta Tab 868 pro: {e}")
        return

    # ===== الاشتراكات والإشعارات =====
    # ===== نظام الإشعارات الذكي والمربوط بالفايربيز =====
    elif cd == "unsubscribe_me":
        try:
            if db:
                # تحديث حالة الإشعارات في الفايربيز إلى False فوراً لمنع الإرسال له
                db.collection('users').document(str(user_id)).set({"is_subscribed": False}, merge=True)
            bot.answer_callback_query(call.id, "🚫 تم إلغاء الاشتراك!")
            
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("✅ إعادة تفعيل الإشعارات", callback_data="resubscribe_me"))
            bot.edit_message_text("🚫 **تم إيقاف الإشعارات بنجاح.**\n\nلن تصلك أي رسائل جماعية أو تحديثات بعد الآن إلا إذا قمت بإعادة تفعيلها من الزر أدناه:", 
                                  call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        except Exception as e:
            print(f"Error in unsubscribe_me: {e}")
            bot.answer_callback_query(call.id, "❌ حدث خطأ أثناء الحفظ.")
        return

    elif cd == "resubscribe_me":
        try:
            if db:
                # إعادة حالة الإشعارات إلى True في حال رغب المستخدم في العودة
                db.collection('users').document(str(user_id)).set({"is_subscribed": True}, merge=True)
            bot.answer_callback_query(call.id, "✅ تم التفعيل بنجاح!")
            bot.edit_message_text("✅ **أهلاً بك مجدداً!**\n\nتم إعادة تفعيل الإشعارات، وستصلك رسائل التعميم والتحديثات فور صدورها.", 
                                  call.message.chat.id, call.message.message_id, parse_mode="Markdown")
        except Exception as e:
            print(f"Error in resubscribe_me: {e}")
        return

    # ===== الملف الشخصي والقائمة =====
    elif cd == "back_start":
        try: bot.delete_message(user_id, call.message.message_id)
        except: pass
        show_main_menu(user_id)

    elif cd == "my_profile":
        try: bot.delete_message(user_id, call.message.message_id)
        except: pass
        show_my_profile(user_id)

   
    # ===== 🌟 نظام تقييم البوت التفاعلي بالعرض مع إظهار التقييم الحالي للأعضاء 🌟 =====
    elif cd == "my_interactions":
        try: bot.delete_message(user_id, call.message.message_id)
        except: pass
        show_my_interactions(user_id)

    # ===== 🌟 نظام التقييم الديناميكي الحقيقي + إحصائيات المشتركين الحية مية بالمية 🌟 =====
    elif cd == "rate_bot_menu":
        try: bot.answer_callback_query(call.id)
        except: pass
        
        # تهيئة العدادات البرمجية لحساب متوسط تقييم البوت فورا من قاعدة البيانات حَقك
        total_stars = 0
        rating_count = 0
        avg_rating_text = "5.0 / 5 ⭐" 
        total_users = 0
        banned_count = 0
        active_users = 0
        
        try:
            if db:
                # جلب أعداد المشتركين الحية بالاعتماد على نفس هيكلة دالات الإحصائيات في كودك
                total_users = db.collection('users').count().get()[0][0].value
                banned_count = db.collection('users').where('is_banned', '==', 1).count().get()[0][0].value
                active_users = total_users - banned_count

                # حساب متوسط التقييم الفعلي من الفايربيز
                rated_users_ref = db.collection('users').where('user_rating', '>', 0).stream()
                for u_doc in rated_users_ref:
                    total_stars += u_doc.to_dict().get('user_rating', 0)
                    rating_count += 1
                
                if rating_count > 0:
                    avg_rating_text = f"{(total_stars / rating_count):.1f} / 5 ⭐"
        except Exception as e:
            print(f"❌ خطأ أثناء حساب الإحصائيات الحية لواجهة العميل: {e}")

        markup = types.InlineKeyboardMarkup()
        markup.row(types.InlineKeyboardButton("⭐", callback_data="set_rate_1"))
        markup.row(types.InlineKeyboardButton("⭐⭐", callback_data="set_rate_2"))
        markup.row(types.InlineKeyboardButton("⭐⭐⭐", callback_data="set_rate_3"))
        markup.row(types.InlineKeyboardButton("⭐⭐⭐⭐", callback_data="set_rate_4"))
        markup.row(types.InlineKeyboardButton("⭐⭐⭐⭐⭐", callback_data="set_rate_5"))
        
        markup.row(types.InlineKeyboardButton("🔙 رجوع للقائمة", callback_data="back_start"))
        
        # عرض البيانات والإحصائيات الحقيقية تماماً لإثبات مصداقية وقوة البوت أمام المستخدم
        display_text = (
            f"📊 **إحصائيات ومصداقية منظومة HMAX:**\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"⭐ **التقييم العام الفعلي للبوت:** `{avg_rating_text}`\n"
            f"👥 **إجمالي المشتركين الكلي:** `{total_users}` عضو مسجل\n"
            f"🟢 **المستخدمين النشطين الآن:** `{active_users}` فني ومبرمج\n"
            f"🚫 **الحسابات المعطلة والمحظورة:** `{banned_count}` حساب\n"
            f"💬 **عدد الأعضاء المقيمين للخدمة:** `{rating_count}` مستخدم\n"
            f"━━━━━━━━━━━━━━━━━━\n\n"
            f"⭐ **رأيك يهمنا لتطوير البوت!**\n"
            f"يسعدنا جداً أن تضع تقييمك الخاص بالأسفل بناءً على تجربتك الشخصية معنا لمساعدتنا على تقديم أفضل الأدوات دائماً.\n"
            f"🎁 **مكافأة التفاعل:** ستحصل على **+15 نقطة** مجانية في رصيدك الموحد عند إتمام تقييمك الأول معنا! 👇"
        )
        bot.edit_message_text(display_text, user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        return

    elif cd.startswith("set_rate_"):
        stars_count = int(cd.replace("set_rate_", ""))
        try:
            if db:
                user_ref = db.collection('users').document(str(user_id))
                user_doc = user_ref.get()
                
                already_rated = False
                if user_doc.exists:
                    already_rated = "user_rating" in user_doc.to_dict()
                
                # حفظ النجوم في مستند المستخدم بالفايربيز
                user_ref.set({
                    "user_rating": stars_count,
                    "rating_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }, merge=True)
                
                bonus_text = ""
                if not already_rated:
                    add_points(user_id, 15) # استخدام دالة add_points الأصلية حَقّك بنجاح لمنحه 15 نقطة
                    bonus_text = "\n🎁 تم منحك **+15 نقطة** مكافأة في حسابك رصيدك الموحد!"
                    log_interaction(user_id, f"تقييم البوت بـ {stars_count} نجوم")
                
                # إشعار الإنذار المبكر للأدمن في حال كان التقييم منخفضاً جداً لحل مشكلته فوراً
                alert_badge = "⚠️ تنبيه: تقييم منخفض جداً!" if stars_count <= 2 else "⭐ تقييم جديد"
                
                # إشعار فوري لغرفتك كـ أدمن بالتقييم الجديد
                bot.send_message(
                    MY_CHAT_ID,
                    f"🔔 <b>{alert_badge}</b>\n\n"
                    f"👤 المستخدم صاحب الآيدي: <code>{user_id}</code>\n"
                    f"⭐ التقييم الممنوح: <code>{stars_count}</code> نجوم من 5",
                    parse_mode="HTML"
                )
            
            # فتح شاشة كتابة المقترح/التعليق النصي الاختياري الفخم بعد اختيار النجوم
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(
                types.InlineKeyboardButton("✍️ إضافة مقترح/تعليق نصي للمطور", callback_data=f"write_rate_comment_{stars_count}"),
                types.InlineKeyboardButton("🏠 إنهاء والعودة للرئيسية", callback_data="back_start")
            )
            
            bot.edit_message_text(
                f"🎉 **تم تسجيل تقييمك بنجاح ({stars_count} نجوم)!**{bonus_text}\n\n"
                f"شكراً لمساهمتك معنا، هل تود كتابة مقترح أو رسالة نصية قصيرة للإدارة حول تجربتك؟",
                user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown"
            )
        except Exception as e:
            print(f"Error in saving rate: {e}")
            try: bot.answer_callback_query(call.id, "❌ حدث خطأ أثناء حفظ تقييمك.")
            except: pass
        return

    elif cd.startswith("write_rate_comment_"):
        stars = cd.replace("write_rate_comment_", "")
        try: bot.delete_message(user_id, call.message.message_id)
        except: pass
        
        msg = bot.send_message(user_id, "✍️ **يرجى كتابة مقترحك أو تعليقك الآن في رسالة وإرسالها فورا فورا (أو اكتب 'إلغاء'):**")
        bot.register_next_step_handler(msg, save_rating_comment_step, stars)
        return

    # ===== 🎁 قسم هدية لكم (من الأزرار الشفافة) =====
    elif cd == "gift_section":
        try: bot.answer_callback_query(call.id)
        except: pass
        
        try:
            log_interaction(user_id, "دخول قسم الهدايا")
        except:
            pass
            
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("📱 عرض شاشة الآيفون على الكمبيوتر مجاناً + تفعيل", callback_data="gift_iphone_screen_mirror"),
            types.InlineKeyboardButton("🎬 أفضل برنامج لتصوير شاشة اللابتوب", callback_data="gift_screen_recorder"),
            types.InlineKeyboardButton("💢 أداة تخطي الآيكلاود مجاناً لمعالجات A5 (تجريبي)", callback_data="gift_icloud_a5"),
            types.InlineKeyboardButton("📺 برنامج للايفون لمشاهدة قنوات كاس العالم مجانا", callback_data="iphone_worldcup_app"),
            types.InlineKeyboardButton("🎁 Adobe Creative Cloud", callback_data="adobe_cloud_gift"),
            types.InlineKeyboardButton("🎁 FRP SAMSUNG All Model EXYNOS", callback_data="page_gift_samsung_exynos"),
            types.InlineKeyboardButton("🔍 بوت كاشف الأرقام", callback_data="number_detector"),
            types.InlineKeyboardButton("🎁 FMI OFF - Open Menu", callback_data="gift_fmi_off"),
            types.InlineKeyboardButton("📱 تخطي الايفون 1/9/2026 iOS 9.0x الى iOS 27.x", callback_data="gift_iphone_bypass"),
            types.InlineKeyboardButton("🔙 رجوع", callback_data="back_start")
        )
        
        try:
            bot.edit_message_text(
                "🎁 **قسم هدية لكم:**\nأفضل الحلول الحصرية والمجانية بين يديك:",
                call.message.chat.id, call.message.message_id, 
                reply_markup=markup, parse_mode="Markdown"
            )
        except Exception as e:
            print(f"❌ خطأ في فتح قسم الهدايا: {e}")
        return

    # ===== 📁 القائمة الرئيسية: DUMP+Scatter Samsung =====
    elif cd == "dump_scatter_samsung":
        try: bot.answer_callback_query(call.id)
        except: pass
        lang = hmaxi18n.get_language(user_id)
        samsung_dump_menu = {
            "ar": {
                "title": (
                    "📁 **قسم ملفات DUMP + Scatter Samsung**\n"
                    "━━━━━━━━━━━━━━━━━━\n"
                    "اختر الموديل المطلوب لعرض تفاصيل الفلاشة وروابط التحميل:"
                ),
                "a146u1": "🛠️ إحياء هاتف SAMSUNG SM-A146U1",
                "a075f": "⚡ A075FXXU1AYG6 DUMP [قديم]",
                "a075f_new": "🔥 A07 4G SM-A075F Android 16 - A075FXXS6CZF6 - NEW",
                "x216b": "💾 Dump X216b XXUD",
                "a125f": "📱 SAMSUNG A12 – SM-A125F [DUMP]",
                "a256e": "📱 SAMSUNG A25 5G – SM-A256E [DUMP]",
                "back": "🔙 العودة لقائمة الـ DUMP",
            },
            "en": {
                "title": (
                    "📁 **Samsung DUMP + Scatter Files**\n"
                    "━━━━━━━━━━━━━━━━━━\n"
                    "Select the model to view firmware details and download links:"
                ),
                "a146u1": "🛠️ SAMSUNG SM-A146U1 Revive Firmware",
                "a075f": "⚡ A075FXXU1AYG6 DUMP [OLD]",
                "a075f_new": "🔥 A07 4G SM-A075F Android 16 - A075FXXS6CZF6 - NEW",
                "x216b": "💾 Dump X216b XXUD",
                "a125f": "📱 SAMSUNG A12 – SM-A125F [DUMP]",
                "a256e": "📱 SAMSUNG A25 5G – SM-A256E [DUMP]",
                "back": "🔙 Back to DUMP list",
            },
            "fr": {
                "title": (
                    "📁 **Fichiers DUMP + Scatter Samsung**\n"
                    "━━━━━━━━━━━━━━━━━━\n"
                    "Sélectionnez le modèle pour afficher les détails et les liens de téléchargement :"
                ),
                "a146u1": "🛠️ Réparation SAMSUNG SM-A146U1",
                "a075f": "⚡ A075FXXU1AYG6 DUMP [ANCIEN]",
                "a075f_new": "🔥 A07 4G SM-A075F Android 16 - A075FXXS6CZF6 - NOUVEAU",
                "x216b": "💾 Dump X216b XXUD",
                "a125f": "📱 SAMSUNG A12 – SM-A125F [DUMP]",
                "a256e": "📱 SAMSUNG A25 5G – SM-A256E [DUMP]",
                "back": "🔙 Retour à la liste DUMP",
            },
        }
        samsung_labels = samsung_dump_menu.get(lang, samsung_dump_menu["ar"])
        display_text = samsung_labels["title"]
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton(samsung_labels["a146u1"], callback_data="dump_a146u1"),
            types.InlineKeyboardButton(samsung_labels["a075f"], callback_data="dump_a075f"),
            types.InlineKeyboardButton(samsung_labels["a075f_new"], callback_data="dump_a075f_new"),
            types.InlineKeyboardButton(samsung_labels["x216b"], callback_data="dump_x216b_xxud"),
            types.InlineKeyboardButton(samsung_labels["a125f"], callback_data="dump_a125f"),
            types.InlineKeyboardButton(samsung_labels["a256e"], callback_data="dump_a256e"),
            types.InlineKeyboardButton(samsung_labels["back"], callback_data="dump_main_section")
        )
        
        _hmax_show_menu(call, display_text, markup, parse_mode="Markdown")
        return

    # Retain the legacy callback for Samsung keyboards already sent to users.
    elif cd in ("dump_model_tab_a9_sm_x110", "dump_model_samsung_tab_a9_sm_x110"):
        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass
        try:
            bot.delete_message(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
            )
        except Exception as e:
            print(f"Delete SAMSUNG Tab A9 menu failed: {e}")

        txt = (
            "📱 Samsung Galaxy Tab A9 - FULL DUMP 📱\n"
            "━━━━━━━━━━━━\n"
            "📱 Device: Samsung Galaxy Tab A9\n"
            "🏷️ Model: SM-X110\n"
            "🏗️ Build: X110XXS6CYI3\n"
            "📦 File: FULL DUMP\n"
            "🔧 Read By: UnlockTool\n"
            "📚 Library: DUMPING-FIRMWARE\n"
            "☁️ Upload: Google Drive\n"
            "━━━━━━━━━━━━\n"
            "⚠️ مهم: تأكد من تطابق SM-X110 و X110XXS6CYI3 قبل الكتابة\n"
            "🔐 Pass: MobiFirmware.VIP"
        )
        txt = _dump_card_text(user_id, "dump_model_tab_a9_sm_x110", txt)
        photo_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "images",
            "samsung_tab_a9_sm_x110_full_dump.jpg",
        )
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton(
            _dump_btn(user_id, "📥 Download - Google Drive"),
            url="https://drive.google.com/file/d/199DEolDruK6iP3oh6iGJ9XkOJWJsDqil/view",
        ))
        markup.add(types.InlineKeyboardButton(
            _dump_btn(user_id, "⬅️ Back to TAB"),
            callback_data="dump_tab_section",
        ))
        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(
                    call.message.chat.id,
                    photo,
                    caption=txt,
                    reply_markup=markup,
                )
        except Exception as e:
            print(f"Send SAMSUNG Tab A9 photo failed: {e}")
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    # ===== 1️⃣ الخيار الأول: SAMSUNG SM-A146U1 =====
    elif cd == "dump_a146u1":
        try: bot.answer_callback_query(call.id)
        except: pass
        
        display_text = (
            "🛠️ **فلاشة إحياء هاتف SAMSUNG SM-A146U1**\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "📌 **بيانات الإصدار والملاحظات:**\n"
            "• **الإصدار:** `A146U1UEUDEYF5`\n"
            "• **التاريخ:** 25 يوليو 2025\n"
            "• الفلاشة مجربة شخصياً ومع الزميل هشام محرم.\n\n"
            "⚠️ **تنبيه هام:** يرجى سحب ملفات الشبكة من الهاتف قبل البدء بعملية التفليش.\n"
            "━━━━━━━━━━━━━━━━━━"
        )
        display_text = _dump_card_text(user_id, "dump_a146u1", display_text)
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton(_dump_btn(user_id, "📥 تحميل فلاشة DUMP SM-A146U1"), url="https://www.mediafire.com/file_premium/hos3d6lm6b4fsem/Samsung_SM-A146U1_DUMP_%25282026-8-25_8-57-43%2529.zip/file?fbclid=IwcGRvZgVleHRuA2FlbQIxMABicmlkETFSelROcGZZS0oxeFJ1S3Fyc3J0YwZhcHBfaWQQMjIyMDM5MTc4ODIwMDg5MgABHkECTvOhZB2Lf_-tpN12M-AP5rvQ0FI0tqWT3WuVkGKgUA289TI3Q4NWXGIm_aem_Z5VNzo22zoKG3tW3s_Ai9Q"),
            types.InlineKeyboardButton(_dump_btn(user_id, "🔙 العودة لقائمة سامسونج DUMP"), callback_data="dump_scatter_samsung")
        )
        
        try:
            bot.edit_message_text(display_text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        except Exception as e:
            print(f"❌ خطأ: {e}")
        return

    # ===== 2️⃣ الخيار الثاني: A075FXXU1AYG6 DUMP =====
    elif cd == "dump_a075f":
        try: bot.answer_callback_query(call.id)
        except: pass
        
        display_text = (
            "⚡ **فلاشة كاملة DUMP لهاتف A075F (A075FXXU1AYG6)**\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "📌 **تفاصيل الحل:**\n"
            "حل نهائي لمشكلة انطفاء جهاز A075F بعد التفليش أو عند استخدام فلاشات السكاتر.\n\n"
            "• تم رفع ملف **DUMP كامل** لإعادة إحياء الجهاز بنجاح.\n"
            "• **طريقة التفليش:** يتم التفليش عبر أداة **TSM**.\n"
            "━━━━━━━━━━━━━━━━━━"
        )
        display_text = _dump_card_text(user_id, "dump_a075f", display_text)
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton(_dump_btn(user_id, "📥 تحميل ملف DUMP (Mega)"), url="https://mega.nz/file/qlRy2I4S#-6N_7i99hCGswx5ZwScoTILzk3k2Pn1gBEUrB-sVQ-0"),
            types.InlineKeyboardButton(_dump_btn(user_id, "📺 شرح طريقة التفليش بالفيديو"), url="https://youtu.be/QZNVMxA6g3Y?si=0oa8zkU0y-SH-jy9"),
            types.InlineKeyboardButton(_dump_btn(user_id, "🔙 العودة لقائمة سامسونج DUMP"), callback_data="dump_scatter_samsung")
        )
        
        try:
            bot.edit_message_text(display_text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        except Exception as e:
            print(f"❌ خطأ: {e}")
        return


    

    # ===== SAMSUNG A07 4G - SM-A075F (Android 16) - A075FXXS6CZF6 (NEW) =====
    elif cd == "dump_a075f_new":
        try: bot.answer_callback_query(call.id)
        except: pass
        lang = hmaxi18n.get_language(user_id)
        gdrive_url = "https://drive.google.com/file/d/1YCwzU2B9XZlQK-A-zDNhbLpWpWxwFnAP/view"
        a075f_new_translations = {
            "ar": {
                "details": (
                    "🔥 Samsung Galaxy A07 4G - SM-A075F 🔥\n"
                    "━━━━━━━━━━━━\n"
                    "📱 اصدار الهاتف: B(Android 16)\n"
                    "🔒 حماية الهاتف: A075FXXS6CZF6\n"
                    "🔨 تم سحب الدامب بواسطة UnlockTool\n"
                    "🔐 الملف محمي بكلمة مرور: MobiFirmware.VIP\n"
                    "━━━━━━━━━━━━\n"
                    "خلصنا احنا كدا لا طبعا\n"
                    "تعالا نحمل الملف 👇\n"
                    "━━━━━━━━━━━━\n"
                    "📦 Model: SM-A075F\n"
                    "💾 Type: Full Dump\n"
                    "☁️ Google Drive FREE\n"
                    "HMAX-UNLOCKER - HithamMax"
                ),
                "download": "📥 تحميل A07 4G Android 16 - A075FXXS6CZF6",
                "back": "⬅️ رجوع لـ Samsung",
            },
            "en": {
                "details": (
                    "🔥 Samsung Galaxy A07 4G - SM-A075F 🔥\n"
                    "📱 Version: B(Android 16)\n"
                    "🔒 Security: A075FXXS6CZF6\n"
                    "🔨 Dumped by UnlockTool\n"
                    "🔐 Password: MobiFirmware.VIP\n"
                    "📦 Model: SM-A075F Full Dump Google Drive FREE\n"
                    "HMAX-UNLOCKER"
                ),
                "download": "📥 Download A07 4G Android 16",
                "back": "⬅️ Back to Samsung",
            },
            "fr": {
                "details": (
                    "🔥 Samsung Galaxy A07 4G - SM-A075F 🔥\n"
                    "📱 Version: B(Android 16)\n"
                    "🔒 Sécurité: A075FXXS6CZF6\n"
                    "🔨 Dump par UnlockTool\n"
                    "🔐 Mot de passe: MobiFirmware.VIP\n"
                    "📦 Model: SM-A075F Full Dump Google Drive GRATUIT\n"
                    "HMAX-UNLOCKER"
                ),
                "download": "📥 Télécharger A07 4G Android 16",
                "back": "⬅️ Retour à Samsung",
            },
        }
        a075f_new_labels = a075f_new_translations.get(lang, a075f_new_translations["ar"])
        photo_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "images",
            "samsung_a07_4g_sm_a075f_android16_hmax.jpg",
        )

        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton(a075f_new_labels["download"], url=gdrive_url),
            types.InlineKeyboardButton(a075f_new_labels["back"], callback_data="dump_scatter_samsung"),
        )

        try:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except Exception as e:
            print(f"Delete SAMSUNG A07 4G menu failed: {e}")

        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(
                    call.message.chat.id,
                    photo,
                    caption=a075f_new_labels["details"],
                    reply_markup=markup,
                )
        except Exception as e:
            print(f"Send SAMSUNG A07 4G SM-A075F photo failed: {e}")
            bot.send_message(call.message.chat.id, a075f_new_labels["details"], reply_markup=markup)

        return

    # ===== 💾 تفاصيل Dump X216b XXUD =====
    elif cd == "dump_x216b_xxud":
        try: bot.answer_callback_query(call.id)
        except: pass
        
        display_text = (
            "📦 **Dump X216b XXUD**\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "\n"
            "السلام عليكم ورحمة الله وبركاته\n"
            "\n"
            "🎁 هدية من المهندس Abdullah Ghanem.\n"
            "دامب XML لهاتف Samsung X216B XXUD على آخر حماية.\n"
            "\n"
            "🕊️ نرجو الدعاء لوالده بالرحمة والمغفرة.\n"
            "\n"
            "⚠️ **تنبيه مهم:** يجب سحب ملفات الشبكة أولاً قبل استخدام الدامب.\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "استخدم أزرار التحميل أدناه:"
        )
        display_text = hmaxi18n.translate_static_content(
            "dump_x216b_xxud", display_text, hmaxi18n.get_language(user_id)
        )
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton(_dump_btn(user_id, "📥 تنزيل Dump X216b XXUD"), url="https://drive.usercontent.google.com/open?id=17G7p16ZkVWq_qllLn_of3zg3L-L_83wh&authuser=0"),
            types.InlineKeyboardButton(_dump_btn(user_id, "🔗 فتح الملف في Google Drive"), url="https://drive.google.com/file/d/17G7p16ZkVWq_qllLn_of3zg3L-L_83wh/view?fbclid=IwY2xjawUpQ4VleHRuA2FlbQIxMABwZG9mBWJyaWQRMVdwQnhVcjd1ZzBvSzNRRUFzcnRjBmFwcF9pZBAyMjIwMzkxNzg4MjAwODkyAAEeCgp8XlaHoN2rBkSWapXOqgYHGF3jWF9aZoh0pgaeZgf-wsO8n2QdYCJw1FA_aem_ZcnTGv3jL3lyBaLq03efHw"),
            types.InlineKeyboardButton(_dump_btn(user_id, "👷 صفحة المهندس Abdullah Ghanem"), url="https://www.facebook.com/AbdullahGhanem13"),
            types.InlineKeyboardButton(_dump_btn(user_id, "🔙 العودة لقائمة سامسونج DUMP"), callback_data="dump_scatter_samsung")
        )
        try:
            bot.edit_message_text(display_text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        except Exception as e:
            print(f"❌ خطأ في عرض Dump X216b XXUD: {e}")
        return

    # ===== 📱 SAMSUNG A12 – SM-A125F DUMP =====
    elif cd == "dump_a125f":
        try: bot.answer_callback_query(call.id)
        except: pass
        lang = hmaxi18n.get_language(user_id)
        gdrive_url = "https://drive.google.com/file/d/1RegTQJUux_RdrozEtt9eFR2bmECEnFq3/view"
        a125f_translations = {
            "ar": {
                "details": (
                    "🔥 **SAMSUNG A12 – SM-A125F | ملف DUMP**\n"
                    "━━━━━━━━━━━━━━━━━━\n"
                    "📱 **الموديل:** SM-A125F\n"
                    "📂 **نوع الملف:** DUMP FILE\n"
                    "🔖 **الإصدار:** `A125FXXS6CXJ1`\n"
                    "🛠️ **تم السحب بواسطة:** EASY JTAG PLUS\n"
                    "📏 **الحجم:** 1.5 GB\n"
                    "☁️ Google Drive\n"
                    "🔑 **كلمة المرور:** MobiFirmware.VIP\n"
                    "━━━━━━━━━━━━━━━━━━"
                ),
                "download": "📥 تحميل – Google Drive",
                "back": "🔙 العودة لقائمة سامسونج DUMP",
            },
            "en": {
                "details": (
                    "🔥 **SAMSUNG A12 – SM-A125F | DUMP FILE**\n"
                    "━━━━━━━━━━━━━━━━━━\n"
                    "📱 **Model:** SM-A125F\n"
                    "📂 **File Type:** DUMP FILE\n"
                    "🔖 **Version:** `A125FXXS6CXJ1`\n"
                    "🛠️ **Dumped With:** EASY JTAG PLUS\n"
                    "📏 **Size:** 1.5 GB\n"
                    "☁️ Google Drive\n"
                    "🔑 **Password:** MobiFirmware.VIP\n"
                    "━━━━━━━━━━━━━━━━━━"
                ),
                "download": "📥 Download – Google Drive",
                "back": "🔙 Back to Samsung DUMP list",
            },
            "fr": {
                "details": (
                    "🔥 **SAMSUNG A12 – SM-A125F | FICHIER DUMP**\n"
                    "━━━━━━━━━━━━━━━━━━\n"
                    "📱 **Modèle :** SM-A125F\n"
                    "📂 **Type de fichier :** DUMP FILE\n"
                    "🔖 **Version :** `A125FXXS6CXJ1`\n"
                    "🛠️ **Extrait avec :** EASY JTAG PLUS\n"
                    "📏 **Taille :** 1.5 GB\n"
                    "☁️ Google Drive\n"
                    "🔑 **Mot de passe :** MobiFirmware.VIP\n"
                    "━━━━━━━━━━━━━━━━━━"
                ),
                "download": "📥 Télécharger – Google Drive",
                "back": "🔙 Retour à la liste Samsung DUMP",
            },
        }
        a125f_labels = a125f_translations.get(lang, a125f_translations["ar"])
        display_text = a125f_labels["details"]
        photo_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "images",
            "samsung_a12_a125f.png",
        )

        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton(a125f_labels["download"], url=gdrive_url),
            types.InlineKeyboardButton(a125f_labels["back"], callback_data="dump_scatter_samsung")
        )

        try:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except Exception as e:
            print(f"Delete SAMSUNG A12 model menu failed: {e}")

        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(
                    call.message.chat.id,
                    photo,
                    caption=display_text,
                    reply_markup=markup,
                    parse_mode="Markdown",
                )
        except Exception as e:
            print(f"Send SAMSUNG A12 SM-A125F photo failed: {e}")
            bot.send_message(call.message.chat.id, display_text, reply_markup=markup, parse_mode="Markdown")

        return

    # ===== 📱 SAMSUNG A25 5G – SM-A256E DUMP =====
    elif cd == "dump_a256e":
        try: bot.answer_callback_query(call.id)
        except: pass
        lang = hmaxi18n.get_language(user_id)
        gdrive_url = "https://drive.google.com/file/d/1Tw19y4kZPm8mHaO0raheL4nIfp3_HUv2/view"
        a256e_translations = {
            "ar": {
                "details": (
                    "📋 **بطاقة مواصفات الفيرموير**\n"
                    "━━━━━━━━━━━━━━━━━━━━\n"
                    "📱 **الجهاز:** SAMSUNG A25 5G\n"
                    "🔢 **الموديل:** SM-A256E\n"
                    "💾 **التخزين:** 128GB UFS\n"
                    "🔖 **إصدار الدامب:** `A256EXXS8CYG3`\n"
                    "🛠️ **تم السحب بواسطة:** F64 ULTRA\n"
                    "📏 **حجم الدامب:** 4.5 GB\n"
                    "📂 **نوع الملف:** RAR\n"
                    "🔑 **كلمة المرور:** MobiFirmware.VIP\n"
                    "☁️ **السيرفر:** Google Drive\n"
                    "━━━━━━━━━━━━━━━━━━━━"
                ),
                "download": "📥 تحميل - Google Drive",
                "back": "🔙 العودة لقائمة سامسونج DUMP",
            },
            "en": {
                "details": (
                    "📋 **FIRMWARE SPEC CARD**\n"
                    "━━━━━━━━━━━━━━━━━━━━\n"
                    "📱 **Device:** SAMSUNG A25 5G\n"
                    "🔢 **Model:** SM-A256E\n"
                    "💾 **Storage:** 128GB UFS\n"
                    "🔖 **Dump Version:** `A256EXXS8CYG3`\n"
                    "🛠️ **Dumped With:** F64 ULTRA\n"
                    "📏 **Dump Size:** 4.5 GB\n"
                    "📂 **File Type:** RAR\n"
                    "🔑 **Password:** MobiFirmware.VIP\n"
                    "☁️ **Server:** Google Drive\n"
                    "━━━━━━━━━━━━━━━━━━━━"
                ),
                "download": "📥 Download - Google Drive",
                "back": "🔙 Back to Samsung DUMP list",
            },
            "fr": {
                "details": (
                    "📋 **FICHE TECHNIQUE DU FIRMWARE**\n"
                    "━━━━━━━━━━━━━━━━━━━━\n"
                    "📱 **Appareil :** SAMSUNG A25 5G\n"
                    "🔢 **Modèle :** SM-A256E\n"
                    "💾 **Stockage :** 128GB UFS\n"
                    "🔖 **Version du dump :** `A256EXXS8CYG3`\n"
                    "🛠️ **Extrait avec :** F64 ULTRA\n"
                    "📏 **Taille du dump :** 4.5 GB\n"
                    "📂 **Type de fichier :** RAR\n"
                    "🔑 **Mot de passe :** MobiFirmware.VIP\n"
                    "☁️ **Serveur :** Google Drive\n"
                    "━━━━━━━━━━━━━━━━━━━━"
                ),
                "download": "📥 Télécharger - Google Drive",
                "back": "🔙 Retour à la liste Samsung DUMP",
            },
        }
        a256e_labels = a256e_translations.get(lang, a256e_translations["ar"])
        display_text = a256e_labels["details"]
        photo_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "images",
            "samsung_a25_a256e.png",
        )

        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton(a256e_labels["download"], url=gdrive_url),
            types.InlineKeyboardButton(a256e_labels["back"], callback_data="dump_scatter_samsung")
        )

        try:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except Exception as e:
            print(f"Delete SAMSUNG A25 model menu failed: {e}")

        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(
                    call.message.chat.id,
                    photo,
                    caption=display_text,
                    reply_markup=markup,
                    parse_mode="Markdown",
                )
        except Exception as e:
            print(f"Send SAMSUNG A25 SM-A256E photo failed: {e}")
            bot.send_message(call.message.chat.id, display_text, reply_markup=markup, parse_mode="Markdown")

        return

    elif cd == "dump_allcall_magic_section":
        markup = types.InlineKeyboardMarkup(row_width=1)
        txt = _dump_localize(user_id, "📱 *ALLCALL MAGIC*\n\nSelect model:")
        markup.add(types.InlineKeyboardButton(
            _dump_btn(user_id, "🔥 ALLCALL MAGIC 60 - EXCLUSIVE DUMP"),
            callback_data="dump_model_allcall_magic_60_exclusive",
        ))
        markup.add(types.InlineKeyboardButton(_dump_back_label(user_id, "🔙 Back"), callback_data="dump_main_section"))
        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass
        _hmax_show_menu(call, txt, markup, parse_mode="Markdown")
        return

    elif cd == "dump_model_allcall_magic_60_exclusive":
        try:
            bot.answer_callback_query(call.id)
        except:
            pass
        lang = hmaxi18n.get_language(user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        gdrive_url = "https://drive.google.com/file/d/16LeQjY7x-slLFuftE9DVFrtBdvmfCvqx/view"
        try:
            bot.delete_message(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
            )
        except:
            pass
        if lang == "en":
            txt = (
                "🔥📱 EXCLUSIVE DUMP - ALLCALL MAGIC 60\n"
                "You will not find this dump online\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n"
                "📌 Dump Version:\n"
                "EG_AOS14.0_28.05.2025\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n"
                "🛠️ Dumped With:\n"
                "Pandora Tool\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n"
                "❤️ Special Thanks to Eng. Abdullah Ghanem\n"
                "For his great effort in dumping\n"
                "🌹 JazakAllah Khair\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n"
                "☁️ Uploaded on Google Drive\n"
                "🔐 Password: MobiFirmware.VIP\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n"
                "📞 https://wa.me/message/A3KQWHSSERCFG1\n"
            )
        else:
            txt = (
                "🔥📱 دامب حصري ALLCALL MAGIC 60\n"
                "لن تجده عبر الانترنت\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n"
                "📌 إصدار الدامب:\n"
                "EG_AOS14.0_28.05.2025\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n"
                "🛠️ تم السحب بواسطة:\n"
                "Pandora Tool\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n"
                "❤️ شكر للمهندس عبدالله غانم\n"
                "على مجهوده في سحب ورفع الدامب\n"
                "🌹 جزاه الله خيرًا\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n"
                "☁️ مرفوع على Google Drive\n"
                "🔐 كلمة المرور: MobiFirmware.VIP\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n"
                "📞 https://wa.me/message/A3KQWHSSERCFG1\n"
            )
        txt = _dump_card_text(user_id, "dump_model_allcall_magic_60_exclusive", txt)
        markup.add(types.InlineKeyboardButton(
            _dump_btn(user_id, "📥 Download - Google Drive"),
            url=gdrive_url,
        ))
        markup.add(types.InlineKeyboardButton(
            _dump_back_label(user_id, "🔙 Back"),
            callback_data="dump_allcall_magic_section",
        ))
        bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    # ===== قسم KXD الجديد =====
    elif cd == "dump_kxd_section":
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "1. KXD A07 — Android 13 [3GB]"), callback_data="dump_kxd_a07_a13"))
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "2. KXD A07 — Android 12 [2.2GB]"), callback_data="dump_kxd_a07_a12"))
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "⬅️ Back to DUMP"), callback_data="dump_main_section"))
        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass
        _hmax_show_menu(call, _dump_localize(user_id, "📱 KXD - Firmware Library\nوفرنا إصدارين مختلفين من KXD A07:"), markup)
        return

    elif cd == "dump_kxd_a07_a13":
        markup = types.InlineKeyboardMarkup(row_width=1)
        gdrive_url = "https://drive.google.com/file/d/1SqGxl0jvG9OYeE-A0zXnJusk2kTS7xGB/view"
        photo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", "kxd_a07_dual_hmax.jpg")
        try:
            bot.answer_callback_query(call.id)
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except Exception:
            pass
        txt = (
            "🔥 وفرنا إصدارين مختلفين من KXD A07\n"
            "━━━━━━━━━━━━\n"
            "🟣 DUMP 01\n"
            "KXD A07 — Android 13\n"
            "🔨 Dump By Pandora Tool\n"
            "A07_KXD_A13_V1.263_oy_20250423\n"
            "• Build ID: TP1A.220624.014\n"
            "• Security Patch: 2025-05-05\n"
            "• Firmware: 250411\n"
            "• Platform: SP9863A\n"
            "• Userdata: F2FS\n"
            "💾 الحجم: 3 GB\n"
            "☁️ Google Drive — FREE\n"
            "━━━━━━━━━━━━\n"
            "⚠️ خد بالك يا أخويا الفني ملاحظه\n"
            "النقطة دي أهم من الدامب نفسه.\n"
            "━━━━━━━━━━━━\n"
            "📌 KXD A07 له أكثر من إصدار.\n"
            "يعني مش معنى إن الجهاز اسمه A07 إن أي Dump خاص بـ A07 هيشتغل عليه.\n"
            "قبل ما تضغط Flash:\n"
            " راجع Build ID\n"
            " راجع Display ID\n"
            " راجع إصدار السوفتوير\n"
            " وتأكد إن الدامب مطابق تمامًا للإصدار الموجود على جهازك.\n"
            " ما تعتمدش على اسم الموديل فقط.\n"
            "لأن اختيار ملف غير مطابق ممكن يحول مشكلة سوفت بسيطة إلى مشكلة أكبر أو موت للجهاز.\n"
            "━━━━━━━━━━━━\n"
            "🔐 كلمة مرور الملفات\n"
            "MobiFirmware.VIP\n"
            "━━━━━━━━━━━━\n"
            "HMAX-UNLOCKER - HithamMax\n"
        )
        txt = _dump_card_text(user_id, "dump_kxd_a07_a13", txt)
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📥 DUMP 01 — Android 13 — 3 GB"), url=gdrive_url))
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "⬅️ Back to KXD"), callback_data="dump_kxd_section"))
        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(call.message.chat.id, photo, caption=txt, reply_markup=markup)
        except Exception:
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    elif cd == "dump_kxd_a07_a12":
        markup = types.InlineKeyboardMarkup(row_width=1)
        gdrive_url = "https://drive.google.com/file/d/1hOfF0HqTxCH0NclxiK2eJsg4uS7XPVTb/view"
        photo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", "kxd_a07_dual_hmax.jpg")
        try:
            bot.answer_callback_query(call.id)
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except Exception:
            pass
        txt = (
            "🔥 وفرنا إصدارين مختلفين من KXD A07\n"
            "━━━━━━━━━━━━\n"
            "🟢 DUMP 02\n"
            "KXD A07 — Android 12\n"
            "🔨 Dump By Pandora Tool\n"
            "A07_KXD_V1.03_oy_20230924\n"
            "• Build ID: SP1A.210812.016\n"
            "• Security Patch: 2022-11-05\n"
            "• Firmware: 230103\n"
            "• Platform: SP9863A\n"
            "• Userdata: F2FS\n"
            "💾 الحجم: 2.2 GB\n"
            "☁️ Google Drive — FREE\n"
            "━━━━━━━━━━━━\n"
            "⚠️ خد بالك يا أخويا الفني ملاحظه\n"
            "📌 KXD A07 له أكثر من إصدار.\n"
            "راجع Build ID و Display ID وإصدار السوفتوير قبل التفليش.\n"
            "━━━━━━━━━━━━\n"
            "🔐 كلمة مرور الملفات\n"
            "MobiFirmware.VIP\n"
            "━━━━━━━━━━━━\n"
            "وفي النهاية…\n"
            "إحنا مش بنحاول نجمع ملفات وخلاص.\n"
            "الملف اللي بنوفره النهارده ممكن يكون سبب في إن جهاز يرجع يشتغل بكرة.\n"
            "━━━━━━━━━━━━\n"
            "HMAX-UNLOCKER - HithamMax\n"
        )
        txt = _dump_card_text(user_id, "dump_kxd_a07_a12", txt)
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📥 DUMP 02 — Android 12 — 2.2 GB"), url=gdrive_url))
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "⬅️ Back to KXD"), callback_data="dump_kxd_section"))
        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(call.message.chat.id, photo, caption=txt, reply_markup=markup)
        except Exception:
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    # ===== القسم الجديد AllCall =====
    elif cd == "dump_allcall_section":
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "🔥 AllCall Hero 60 Max - FULL DUMP [UnlockTool] RARE"), callback_data="dump_model_allcall_hero_60_max_full_dump_unlocktool"))
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "⬅️ Back to DUMP"), callback_data="dump_main_section"))
        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass
        _hmax_show_menu(call, _dump_localize(user_id, "📱 AllCall - Firmware Library\nاختر الموديل:"), markup, parse_mode="Markdown")
        return

    elif cd == "dump_model_allcall_hero_60_max_full_dump_unlocktool":
        markup = types.InlineKeyboardMarkup(row_width=1)
        gdrive_url = "https://drive.google.com/file/d/1EsPIC9Wp1h0vWDRA1Gi6k-obUHYGkEqu/view"
        photo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", "allcall_hero_60_max_full_dump_unlocktool_rare_hmax.jpg")
        try:
            bot.answer_callback_query(call.id)
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except Exception:
            pass
        txt = (
            "🔥 *ملف نادر جدًا وصل عندنا… والمرادي لـ AllCall Hero 60 Max!*\n"
            "━━━━━━━━━━━━\n"
            "📱 AllCall Hero 60 Max — FULL DUMP\n"
            "━━━━━━━━━━━━\n"
            "لو بتدور على فلاشة للجهاز ده، فغالبًا عارف إن الملفات النادرة هي اللي بتعمل الفرق وقت ما الجهاز يكون قدامك ومفيش ملف متوفر.\n"
            "━━━━━━━━━━━━\n"
            "🔧 **الملف تم سحبه مباشرة من الجهاز باستخدام UnlockTool**، وتم رفعه وتجهيزه للتحميل عبر Google Drive.\n"
            "━━━━━━━━━━━━\n"
            "📦 تفاصيل الفلاشة:\n"
            "• Model: AllCall Hero 60 Max\n"
            "• Type: Full Dump\n"
            "• Tool: UnlockTool\n"
            "• Hosting: Google Drive\n"
            "• Password: MobiFirmware.VIP\n"
            "━━━━━━━━━━━━\n"
            "💎 دامب لن تجده عبر الإنترنت نهائيًا بالشكل المتوفر هنا.\n"
            "━━━━━━━━━━━━\n"
            "HMAX-UNLOCKER • HithamMax\n"
        )
        txt = _dump_card_text(user_id, "dump_model_allcall_hero_60_max_full_dump_unlocktool", txt)
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📥 Download - Google Drive"), url=gdrive_url))
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "⬅️ Back to AllCall"), callback_data="dump_allcall_section"))
        try:
            with open(photo_path, 'rb') as photo:
                bot.send_photo(call.message.chat.id, photo, caption=txt, reply_markup=markup, parse_mode="Markdown")
        except Exception as e:
            print(f"Photo error: {e}")
            bot.send_message(call.message.chat.id, txt, reply_markup=markup, parse_mode="Markdown")
        return

    elif cd == "dump_realme_section":
        markup = types.InlineKeyboardMarkup(row_width=1)
        txt = _dump_localize(user_id, "📱 *REALME*\n\nSelect model:")
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "🔥 REALME C71 RMX5303 - 7.4GB [PANDORA]"), callback_data="dump_model_realme_c71_rmx5303"))
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "🔥 REALME C15 RMX2180 - 5.6GB [PANDORA]"), callback_data="dump_model_realme_c15_rmx2180"))
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "🟡 NOTE 60X RMX3938 - 64GB eMMC - 2025-10-01 [F64 BOX]"), callback_data="dump_model_realme_note_60x_rmx3938"))
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "🔥 REALME 10 PRO 5G RMX3661 - 256GB UFS [F64 BOX]"), callback_data="dump_model_realme_10_pro_5g_rmx3661"))
        markup.add(types.InlineKeyboardButton(
            _dump_btn(user_id, "🔥 C35 RMX3511 DUMP XML 128GB [EasyJTAG] - Thamer"),
            callback_data="dump_model_realme_c35_rmx3511_xml",
        ))
        markup.add(types.InlineKeyboardButton(
            _dump_btn(user_id, "🔥 C35 RMX3511 FULL DUMP A.55 [Pandora]"),
            callback_data="dump_model_realme_c35_rmx3511_full_a55",
        ))
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "🔥 Note 50 RMX3834 A.89 FULL [PANDORA]"), callback_data="dump_model_realme_note_50_rmx3834_a89"))
        markup.add(types.InlineKeyboardButton(_dump_back_label(user_id, "🔙 Back"), callback_data="dump_main_section"))
        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass
        _hmax_show_menu(call, txt, markup, parse_mode="Markdown")
        return

    elif cd in (
        "dump_model_realme_c35_rmx3511_xml",
        "dump_model_realme_c35_rmx3511_full_a55",
    ):
        is_xml_dump = cd == "dump_model_realme_c35_rmx3511_xml"
        markup = types.InlineKeyboardMarkup(row_width=1)
        if is_xml_dump:
            gdrive_url = "https://drive.google.com/file/d/1YBVx9kAU2yXncW-sc54NZrnHVbCOLVE9/view"
            image_name = "realme_c35_rmx3511_xml_128gb.jpg"
            txt = (
                "📱 Realme C35 - DUMP XML 128GB 📱\n"
                "━━━━━━━━━━━━\n"
                "📱 Device: Realme C35\n"
                "🏷️ Model: RMX3511\n"
                "📦 File: DUMP XML - 128GB\n"
                "🔧 Read By: Easy JTAG Plus\n"
                "👤 بناء على طلب: ثامر زروقي\n"
                "📚 Library: DUMPING-FIRMWARE\n"
                "☁️ Upload: Google Drive\n"
                "━━━━━━━━━━━━\n"
                "🔐 Pass: MobiFirmware.VIP"
            )
        else:
            gdrive_url = "https://drive.google.com/file/d/1L6PYGzOfBmmgazHS7KT-ouc3INAU0cl7/view"
            image_name = "realme_c35_rmx3511_full_dump_a55_pandora.jpg"
            txt = (
                "📱 Realme C35 - FULL DUMP A.55 📱\n"
                "━━━━━━━━━━━━\n"
                "📱 Device: Realme C35\n"
                "🏷️ Model: RMX3511\n"
                "🏗️ Build: A.55\n"
                "📦 File: FULL DUMP\n"
                "🔧 Read By: Pandora Tool\n"
                "📚 Library: DUMPING-FIRMWARE\n"
                "☁️ Upload: Google Drive\n"
                "━━━━━━━━━━━━\n"
                "⚠️ مهم: تأكد من تطابق الموديل والاصدار قبل الكتابة\n"
                "🔐 Pass: MobiFirmware.VIP"
            )

        txt = _dump_card_text(user_id, cd, txt)
        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass
        try:
            bot.delete_message(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
            )
        except Exception as e:
            print(f"Delete Realme C35 menu failed: {e}")

        photo_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "images",
            image_name,
        )
        markup.add(types.InlineKeyboardButton("📥 Download - Google Drive", url=gdrive_url))
        markup.add(types.InlineKeyboardButton("⬅️ Back", callback_data="dump_realme_section"))
        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(
                    call.message.chat.id,
                    photo,
                    caption=txt,
                    reply_markup=markup,
                )
        except Exception as e:
            print(f"Send Realme C35 photo failed: {e}")
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    elif cd == "dump_model_realme_note_60x_rmx3938":
        markup = types.InlineKeyboardMarkup(row_width=1)
        gdrive_url = "https://drive.google.com/file/d/1pcICRDgQ1ZbFP0sCF0aG6wEPSksEBdln/view"
        photo_path = "images/realme_note_60x_rmx3938.jpg"
        try:
            bot.answer_callback_query(call.id)
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except:
            pass
        txt = (
            "🟡 REALME NOTE 60X - DUMP FILE 🟡\n"
            "━━━━━━━━━━━━\n"
            "📱 Device: Realme Note 60X\n"
            "🏷️ Model: RMX3938\n"
            "💾 Storage: 64GB eMMC\n"
            "🛡️ Patch: 2025-10-01\n"
            "🔧 Dump By: F64 BOX\n"
            "━━━━━━━━━━━━\n"
            "🔐 Pass: MobiFirmware.VIP\n"
        )
        txt = _dump_card_text(user_id, "dump_model_realme_note_60x_rmx3938", txt)
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📥 Download - Google Drive"), url=gdrive_url))
        markup.add(types.InlineKeyboardButton(_dump_back_label(user_id, "⬅️ Back"), callback_data="dump_realme_section"))
        try:
            with open(photo_path, 'rb') as photo:
                bot.send_photo(call.message.chat.id, photo, caption=txt, reply_markup=markup)
        except:
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    elif cd == "dump_model_realme_c71_rmx5303":
        lang = hmaxi18n.get_language(user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        gdrive_url = "https://drive.google.com/file/d/1xficluJ65Ny-Vlih9Ys0rBlWk6OKa9Jj/view"

        try:
            bot.answer_callback_query(call.id)
        except:
            pass
        try:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except:
            pass

        if lang == "en":
            txt = (
                "🔥 Realme C71 RMX5303 FULL DUMP 🔥\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n"
                "📌 Dump Version: export_15_C.09\n"
                "🛠️ Dumped With: Pandora Tool\n"
                "📏 Dump Size: 7.4 GB\n"
                "☁️ Google Drive\n"
                "🔐 Pass: MobiFirmware.VIP\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n"
                "📞 https://wa.me/message/A3KQWHSSERCFG1\n"
            )
        else:
            txt = (
                "🔥 ريلمي C71 RMX5303 - فل دامب 🔥\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n"
                "📌 إصدار الدامب: export_15_C.09\n"
                "🛠️ تم السحب: Pandora Tool\n"
                "📏 الحجم: 7.4 GB\n"
                "☁️ Google Drive\n"
                "🔐 كلمة المرور: MobiFirmware.VIP\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n"
                "📞 https://wa.me/message/A3KQWHSSERCFG1\n"
            )
        txt = _dump_card_text(user_id, "dump_model_realme_c71_rmx5303", txt)

        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📥 Download - Google Drive"), url=gdrive_url))
        markup.add(types.InlineKeyboardButton(_dump_back_label(user_id, "🔙 Back"), callback_data="dump_realme_section"))
        bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    elif cd == "dump_model_lake_poco_c75_14c_17c":
        markup = types.InlineKeyboardMarkup(row_width=1)
        gdrive_url = "https://drive.google.com/file/d/1Ki8JkDYwOBdPhDm7OWcGv7s5wvY-fYPj/view"
        photo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images", "poco_c75_redmi_14c_17c_a3_pro_1gb_dump_df.jpg")
        try:
            bot.answer_callback_query(call.id)
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except: pass
        txt = (
            "⭐ lake POCO C75 Redmi 14C REDMI 17C Redmi A3 Pro — دامب 1 جيجا 🔥\n"
            "━━━━━━━━━━━━\n"
            "🙏 كل الشكر والتقدير لأخونا العضو Hossam Khairy\n"
            "على مشاركته معنا الدامب الخاص به\n"
            "━━━━━━━━━━━━\n"
            "📱 POCO C75: Helio G81 Ultra | 6.88\" IPS LCD 120Hz | 720×1640 HD+ | 50MP+AI | 5160mAh 18W | Android 14 HyperOS | 4G LTE\n"
            "📱 Redmi 14C: MediaTek Helio G81 Ultra | 6.88\" IPS LCD 120Hz | 720×1640 HD+ | 50MP+AI | 5160mAh 18W | Android 14 HyperOS\n"
            "📱 REDMI 17C: MediaTek Helio G85 | 6.7\" IPS LCD 90Hz | 720×1600 HD+ | 50MP+AI | 5000mAh 10W | Android 14 HyperOS\n"
            "📱 Redmi A3 Pro: MediaTek Helio G36 | 6.7\" IPS LCD 90Hz | 720×1600 HD+ | 8MP | 5000mAh 10W | Android 14 Go Edition\n"
            "━━━━━━━━━━━━\n"
            "📁 بيانات الملف:\n"
            "Device: POCO C75 / Redmi 14C / REDMI 17C / Redmi A3 Pro\n"
            "File: 1GB DUMP - دامب 1 جيجا مع ملفات الشبكة\n"
            "Pulled By: Flash64 Ultra\n"
            "Upload: Google Drive\n"
            "Pass File: MobiFirmware.VIP\n"
            "━━━━━━━━━━━━\n"
            "HMAX hithamMax - PROFESSIONAL FIRMWARE SOLUTIONS\n"
        )
        txt = _dump_card_text(user_id, "dump_model_lake_poco_c75_14c_17c", txt)
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📥 رابط التحميل - Google Drive"), url=gdrive_url))
        markup.add(types.InlineKeyboardButton(_dump_back_label(user_id, "⬅️ Back"), callback_data="dump_xiaomi_group_section"))
        try:
            with open(photo_path, 'rb') as photo:
                bot.send_photo(call.message.chat.id, photo, caption=txt, reply_markup=markup)
        except Exception as e:
            print(f"Photo error: {e}")
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return

    elif cd == "dump_model_realme_c15_rmx2180":
        lang = hmaxi18n.get_language(user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)

        try:
            bot.answer_callback_query(call.id)
        except:
            pass
        try:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except:
            pass

        if lang == "en":
            txt = (
                "🔥 Realme C15 RMX2180 FULL DUMP 🔥\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n"
                "📌 Dump Version: RMX2180_11_A.26\n"
                "🛠️ Dumped With: Pandora Tool\n"
                "📏 Dump Size: 5.6 GB\n"
                "☁️ Google Drive\n"
                "🔐 Pass: MobiFirmware.VIP\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n"
                "📞 https://wa.me/message/A3KQWHSSERCFG1\n"
            )
        else:
            txt = (
                "🔥 ريلمي C15 RMX2180 - فل دامب 🔥\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n"
                "📌 إصدار الدامب: RMX2180_11_A.26\n"
                "🛠️ تم السحب: Pandora Tool\n"
                "📏 الحجم: 5.6 GB\n"
                "☁️ Google Drive\n"
                "🔐 كلمة المرور: MobiFirmware.VIP\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n"
                "📞 https://wa.me/message/A3KQWHSSERCFG1\n"
            )
        txt = _dump_card_text(user_id, "dump_model_realme_c15_rmx2180", txt)

        markup.add(types.InlineKeyboardButton(_dump_back_label(user_id, "🔙 Back"), callback_data="dump_realme_section"))
        bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return


    elif cd == "dump_model_realme_10_pro_5g_rmx3661":
        markup = types.InlineKeyboardMarkup(row_width=1)
        gdrive_url = "https://drive.google.com/file/d/1a6XXCbruh394KhIMOGDwhmnzZADaSuMV/view"
        photo_path = "images/realme_10_pro_5g_rmx3661.jpg"
        try:
            bot.answer_callback_query(call.id)
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except:
            pass
        txt = (
            "📱 REALME 10 PRO 5G - DUMP FILE 📱\n"
            "━━━━━━━━━━━━\n"
            "📱 Device: REALME 10 PRO 5G\n"
            "🏷️ Model: RMX3661\n"
            "💾 Storage: 256GB UFS\n"
            "🔧 Dump By: F64 BOX\n"
            "━━━━━━━━━━━━\n"
            "🔐 Pass: MobiFirmware.VIP\n"
        )
        txt = _dump_card_text(user_id, "dump_model_realme_10_pro_5g_rmx3661", txt)
        markup.add(types.InlineKeyboardButton(_dump_btn(user_id, "📥 Download - Google Drive"), url=gdrive_url))
        markup.add(types.InlineKeyboardButton(_dump_back_label(user_id, "⬅️ Back"), callback_data="dump_realme_section"))
        try:
            with open(photo_path, 'rb') as photo:
                bot.send_photo(call.message.chat.id, photo, caption=txt, reply_markup=markup)
        except:
            bot.send_message(call.message.chat.id, txt, reply_markup=markup)
        return


    elif cd == "dump_model_realme_note_50_rmx3834_a89":
        try:
            bot.answer_callback_query(call.id)
        except Exception:
            pass
        try:
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        except Exception as e:
            print(f"Delete Realme Note 50 menu failed: {e}")

        lang = hmaxi18n.get_language(user_id)
        gdrive_url = "https://drive.google.com/file/d/10uJP9wiJkrBzGRQIwfjOVcjpCYhAJWoJ/view"
        note50_translations = {
            "ar": {
                "details": (
                    "🌟 Realme Note 50 — RMX3834 — FULL DUMP 🔥\n"
                    "━━━━━━━━━━━━\n"
                    "📁 File:\n"
                    "RMX3834export_13_A.89 DUMP By Pandora Tool\n"
                    "━━━━━━━━━━━━\n"
                    "⚡ Pulled By:\n"
                    "Pandora Tool\n"
                    "━━━━━━━━━━━━\n"
                    "📤 Upload By:\n"
                    "Abdullah Ghanem\n"
                    "━━━━━━━━━━━━\n"
                    "🎯 كل الشكر لأخونا عبدالله غانم\n"
                    "على رفع الملف لإخواننا في الجروب للاستفادة\n"
                    "منه وتوفير حل إضافي للفنيين.\n"
                    "━━━━━━━━━━━━\n"
                    "📱 Device: Realme Note 50 RMX3834\n"
                    "🔢 Version: 13_A.89 - FULL DUMP\n"
                    "🔧 Tool: Pandora Tool\n"
                    "📦 Size: 64GB+ Full Dump Complete\n"
                    "📅 Date: May 2025 - Original Pulled\n"
                    "☁️ Hosting: Google Drive\n"
                    "🔐 Pass File: MobiFirmware.VIP\n"
                ),
                "download": "📥 تحميل - Google Drive",
                "back": "🔙 العودة لقائمة REALME",
            },
            "en": {
                "details": (
                    "🌟 Realme Note 50 — RMX3834 — FULL DUMP 🔥\n"
                    "━━━━━━━━━━━━\n"
                    "📁 File:\n"
                    "RMX3834export_13_A.89 DUMP By Pandora Tool\n"
                    "━━━━━━━━━━━━\n"
                    "⚡ Pulled By:\n"
                    "Pandora Tool\n"
                    "━━━━━━━━━━━━\n"
                    "📤 Upload By:\n"
                    "Abdullah Ghanem\n"
                    "━━━━━━━━━━━━\n"
                    "🎯 Huge thanks to our brother Abdullah Ghanem\n"
                    "for uploading this file for our group members,\n"
                    "giving technicians an extra solution.\n"
                    "━━━━━━━━━━━━\n"
                    "📱 Device: Realme Note 50 RMX3834\n"
                    "🔢 Version: 13_A.89 - FULL DUMP\n"
                    "🔧 Tool: Pandora Tool\n"
                    "📦 Size: 64GB+ Full Dump Complete\n"
                    "📅 Date: May 2025 - Original Pulled\n"
                    "☁️ Hosting: Google Drive\n"
                    "🔐 Pass File: MobiFirmware.VIP\n"
                ),
                "download": "📥 Download - Google Drive",
                "back": "🔙 Back to Realme list",
            },
            "fr": {
                "details": (
                    "🌟 Realme Note 50 — RMX3834 — FULL DUMP 🔥\n"
                    "━━━━━━━━━━━━\n"
                    "📁 Fichier :\n"
                    "RMX3834export_13_A.89 DUMP By Pandora Tool\n"
                    "━━━━━━━━━━━━\n"
                    "⚡ Extrait par :\n"
                    "Pandora Tool\n"
                    "━━━━━━━━━━━━\n"
                    "📤 Mis en ligne par :\n"
                    "Abdullah Ghanem\n"
                    "━━━━━━━━━━━━\n"
                    "🎯 Un grand merci à notre frère Abdullah Ghanem\n"
                    "d'avoir partagé ce fichier avec les membres du groupe,\n"
                    "offrant une solution supplémentaire aux techniciens.\n"
                    "━━━━━━━━━━━━\n"
                    "📱 Appareil : Realme Note 50 RMX3834\n"
                    "🔢 Version : 13_A.89 - FULL DUMP\n"
                    "🔧 Outil : Pandora Tool\n"
                    "📦 Taille : 64GB+ Full Dump Complete\n"
                    "📅 Date : Mai 2025 - Extraction d'origine\n"
                    "☁️ Hébergement : Google Drive\n"
                    "🔐 Mot de passe : MobiFirmware.VIP\n"
                ),
                "download": "📥 Télécharger - Google Drive",
                "back": "🔙 Retour à la liste Realme",
            },
        }
        note50_labels = note50_translations.get(lang, note50_translations["ar"])
        photo_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "images",
            "realme_note_50_rmx3834_a89_dump_pandora.jpg",
        )

        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton(note50_labels["download"], url=gdrive_url))
        markup.add(types.InlineKeyboardButton(note50_labels["back"], callback_data="dump_realme_section"))
        try:
            with open(photo_path, "rb") as photo:
                bot.send_photo(
                    call.message.chat.id,
                    photo,
                    caption=note50_labels["details"],
                    reply_markup=markup,
                )
        except Exception as e:
            print(f"Send Realme Note 50 photo failed: {e}")
            bot.send_message(call.message.chat.id, note50_labels["details"], reply_markup=markup)
        return


    # ===== 🍏 القائمة الفرعية: تخطي الآيفون =====

    # ===== 🍏 القائمة الفرعية: تخطي الآيفون =====
    elif cd == "gift_iphone_bypass":
        try: bot.answer_callback_query(call.id)
        except: pass
        
        text = (
            "🍏 **قسم تخطي الآيفون (iOS 9.0x إلى iOS 27.x)**\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "يرجى اختيار القسم المناسب لجهازك من الخيارات أدناه:"
        )
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("📱 A12 & A13 Bionic (XR to 11 Pro Max, SE2, iPads)", callback_data="iphone_a12_a13"),
            types.InlineKeyboardButton("🔓 iOS 9.0 حتى iOS 26.1 (بدون شبكة)", callback_data="iphone_legacy_bypass"),
            types.InlineKeyboardButton("🔙 العودة لقسم الهدايا", callback_data="gift_section")
        )
        
        try:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        except Exception as e:
            print(f"❌ خطأ: {e}")
        return

    # ===== 📱 الخيار الأول: A12 & A13 Bionic =====
    elif cd == "iphone_a12_a13":
        try: bot.answer_callback_query(call.id)
        except: pass
        
        text = (
            "📱 **A12 & A13 Bionic (XR to 11 Pro Max, SE2, iPads)**\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "📌 **أبرز محطات الإصدار:**\n"
            "• دعم كامل لشرائح Apple A12 و A13 Bionic على iOS 17.x، 18.x، 26.x، و27.x.\n"
            "• تجاوز Hello Bypass بنقرة واحدة مع الحفاظ على الرقم التسلسلي الأصلي (دون تغيير).\n"
            "• مساعد DFU مدمج مع مؤقتات عد تنازلي في الوقت الحقيقي واستغلال BootROM لتقنية USBliter8.\n"
            "• سلسلة إقلاع رامديسك آلية ذات 10 خطوات مع حقن ديناميكي SPTM وTXM.\n"
            "• محرك تركيب مزدوج APFS مع نظام احتياطي تلقائي (طريقة التركيب 2).\n"
            "• معدل رقم تسلسلي مدمج بوضع البنفسجي لتفعيل Hello بديل.\n"
            "• نافذة منبثقة لمعرف Apple ID ورقم الهاتف وقارئ حساب المالك الفوري.\n\n"
            "⚠️ **ملاحظة هامة:** لازم توصيلة خاصة بالآيفون لإدخال الهاتف في وضع PWN.\n"
            "━━━━━━━━━━━━━━━━━━"
        )
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("📥 رابط الأداة", url="https://mega.nz/file/Yi90RBZI#LU-6ncaPvFkce8bAuq5Yj5t8GsAOZRgFcH8mjfHCNLc"),
            types.InlineKeyboardButton("📝 اضغط هنا لتسجيل الجهاز ECID", url="https://iunlock.cloud/register?tool=ramdisk-pro"),
            types.InlineKeyboardButton("📺 فيديو تعليمي", url="https://youtu.be/I2o66eFSKpw?is=1_83NCf5UnGTftoS"),
            types.InlineKeyboardButton("🔙 العودة للقائمة السابقة", callback_data="gift_iphone_bypass")
        )
        
        try:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        except Exception as e:
            print(f"❌ خطأ: {e}")
        return

    # ===== 🔓 الخيار الثاني: iOS 9.0 حتى iOS 26.1 بدون شبكة =====
    elif cd == "iphone_legacy_bypass":
        try: bot.answer_callback_query(call.id)
        except: pass
        
        text = (
            "🔓 **iOS 9.0 حتى iOS 26.1 (بدون شبكة)**\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "📌 **المميزات:**\n"
            "• تجاوز قفل تفعيل iCloud غير متصل مجاناً (A5-A12+).\n"
            "• الإقلاع السريع - ميزة بدء التشغيل السريع لتجاوز التمرير.\n"
            "• تجاوز MDM مجاني مع دعم الإغلاق.\n"
            "• تفعيل رمز المرور - الأدوات الكاملة متوفرة مجاناً.\n"
            "• مفعل CheckM8 Hello لأجهزة A9-A11 (مجاني).\n"
            "• قم بتعطيل تحديثات OTA وأدوات منع إعادة ضبط المصنع.\n"
            "• دعم كامل لمتجر آبل والإشعارات بعد التفعيل.\n"
            "━━━━━━━━━━━━━━━━━━"
        )
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("📥 رابط الأداة", url="https://mega.nz/file/gns1CTYA#Qq4PigKzpZ2INjLMZAbY-7nC26i0Q-7tmTKYRoMfhzU"),
            types.InlineKeyboardButton("📝 موقع رفع السيريال", url="https://iunlock.cloud/register"),
            types.InlineKeyboardButton("🔙 العودة للقائمة السابقة", callback_data="gift_iphone_bypass")
        )
        
        try:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        except Exception as e:
            print(f"❌ خطأ: {e}")
        return

    # ====================================================================================
    # 🎡 المنظومة 1: عجلة الحظ اليومية المتغيرة (Lucky Spin Wheel)
    # ====================================================================================
    elif cd == "lucky_spin_menu":
        try: bot.answer_callback_query(call.id)
        except: pass
        today = str(datetime.date.today())
        
        already_spun = False
        try:
            if db:
                user_doc = db.collection('users').document(str(user_id)).get()
                if user_doc.exists:
                    already_spun = user_doc.to_dict().get('last_lucky_spin', '') == today
        except: pass

        markup = types.InlineKeyboardMarkup()
        if already_spun:
            markup.row(types.InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="back_start"))
            bot.edit_message_text("🎡 **عجلة الحظ اليومية حَقك:**\n\n⚠️ عذراً يا لورد، لقد قمت بلف عجلة الحظ اليوم بالفعل! تفضل بالعودة غداً لتجربة حظك من جديد والحصول على نقاط مجانية حصرية. 💥", user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        else:
            markup.row(types.InlineKeyboardButton("🎡 إبدأ لَف العجلة الآن فورا 🚀", callback_data="spin_wheel_now"))
            markup.row(types.InlineKeyboardButton("🔙 رجوع", callback_data="back_start"))
            bot.edit_message_text("🎡 **مرحباً بك في عجلة الحظ اليومية الحصرية حَق HMAX!**\n\nاضغط على الزر أدناه لتدوير العجلة والحصول على نقاط عشوائية مجانية تضاف فوراً إلى رصيد حسابك الموحد (من 5 إلى 100 نقطة)! ✨🎁", user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        return

    elif cd == "spin_wheel_now":
        today = str(datetime.date.today())
        import random
        prizes = [5, 10, 15, 20, 50, 100]
        won_points = random.choice(prizes)
        
        try:
            if db:
                user_ref = db.collection('users').document(str(user_id))
                user_doc = user_ref.get()
                if user_doc.exists and user_doc.to_dict().get('last_lucky_spin', '') == today:
                    bot.answer_callback_query(call.id, "⚠️ لقد قمت بلف العجلة اليوم سابقاً!", show_alert=True)
                    return
                
                user_ref.set({
                    "last_lucky_spin": today,
                    "points": firestore.Increment(won_points)
                }, merge=True)
                log_interaction(user_id, f"لف عجلة الحظ والفوز بـ {won_points} نقطة")
            
            bot.answer_callback_query(call.id, f"🎉 مبروك! فزت بـ +{won_points} نقطة مجانية!", show_alert=True)
            markup = types.InlineKeyboardMarkup().row(types.InlineKeyboardButton("🏠 العودة للرئيسية", callback_data="back_start"))
            bot.edit_message_text(f"🎯 **مبروك الفوز يا لورد!** 🎉\n\n💥 دارت عجلة الحظ ومنحتك فورا: **+{won_points} نقطة مجانية** تم حقنها بداخل رصيدك بنجاح تام لرفع رتبتك وصناعة التفاعل بداخل المنظومة!", user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        except Exception as e:
            print(f"Error in spin wheel: {e}")
        return

    # ====================================================================================
    # 🛒 المنظومة 2: متجر استبدال وتجميد النقاط المطور (Points Reward Store)
    # ====================================================================================
    elif cd == "points_store_menu":
        try: bot.answer_callback_query(call.id)
        except: pass
        user_pts = get_user_points(user_id)
        
        markup = types.InlineKeyboardMarkup()
        # 🟢 خيار ملف حلب تك بـ 800 نقطة
        markup.row(types.InlineKeyboardButton("🎁 سحب ملف حلب تك مدفوع (800 نقطة)", callback_data="redeem_halabtech"))
        # 💎 خيار عرض جمناي برو المتطور والجديد بـ 3000 نقطة
        markup.row(types.InlineKeyboardButton("💎 عرض جمناي برو + 5 تيرا [18 شهر] (3000 نقطة)", callback_data="redeem_gemini"))
        markup.row(types.InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="back_start"))
        
        bot.edit_message_text(f"🛒 **متجر استبدال مكافآت نقاط HMAX:**\n\nرصيد نقاطك الحالي هو: `{user_pts}` نقطة 🏆\n\n💡 يمكنك الآن تجميد واستبدال رصيد نقاطك مجاناً مقابل خدمات سيرفرية حقيقية! اختر الجائزة المطلوبة أدناه عند توفر رصيد كافٍ حَقك:", user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        return

    elif cd.startswith("redeem_"):
        gift_type = cd.replace("redeem_", "")
        # 📊 الحسبة البرمجية المحدثة للخصم التلقائي حسب اختيار العميل
        cost = 800 if gift_type == "halabtech" else 3000
        gift_name = "سحب ملف حلب تك مدفوع 👑" if gift_type == "halabtech" else "تفعيل عرض جمناي برو + 5 تيرا لمدده 18 شهر 💎"
        
        user_pts = get_user_points(user_id)
        if user_pts < cost:
            bot.answer_callback_query(call.id, f"❌ عذراً، رصيد نقاطك غير كافٍ! تحتاج إلى {cost} نقطة على الأقل.", show_alert=True)
            return
            
        try:
            if db:
                # خصم النقاط الآمن من الفايربيز
                add_points(user_id, -cost)
                log_interaction(user_id, f"استبدال مكافأة: {gift_name}")
                
                # إشعار فوري لغرفتك كـ أدمن مع زر الرد السريع لتسليمه الحساب أو التفعيل
                markup_reply = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("💬 رد وتفعيل فوري", callback_data=f"reply_req_{user_id}"))
                bot.send_message(MY_CHAT_ID, f"🎁 **طلب استبدال مكافأة جديد بالمتجر!**\n\n👤 المستخدم: `{user_id}`\n🛍️ الجائزة المطلوبة: `{gift_name}`\n📉 النقاط المخصومة: `{cost}` نقطة\n\n💡 اضغط على الزر أدناه لتسليمه بيانات العرض فورا:", reply_markup=markup_reply, parse_mode="Markdown")
                
            bot.answer_callback_query(call.id, "🎉 تم تقديم طلب استبدال المكافأة بنجاح تاف!", show_alert=True)
            markup = types.InlineKeyboardMarkup().row(types.InlineKeyboardButton("🏠 العودة للرئيسية", callback_data="back_start"))
            bot.edit_message_text(f"✅ **تم قبول طلب الاستبدال بنجاح يا لورد!**\n\n🛍️ الجائزة: `{gift_name}`\n📉 تم خصم: `-{cost}` نقطة من حسابك.\n\n⏳ جاري تفعيل وتجهيز العرض لك الآن من م/ هيثم ماكس، وسيصلك كود التنشيط بداخل المحادثة هنا فورا بلمح البصر! 🚀🦅", user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        except Exception as e:
            print(f"Error in store redeem: {e}")
        return

    # ====================================================================================
    # 🏆 المنظومة 3: لوحة متصدري الدعوات ونشر البوت (Top Inviters Leaderboard)
    # ====================================================================================
    elif cd == "leaderboard_menu":
        try: bot.answer_callback_query(call.id)
        except: pass
        
        lines = ["🏆 **لوحة الشرف لأعلى متصدري النقاط والدعوات:**\n━━━━━━━━━━━━━━━━━━\n"]
        try:
            if db:
                top_users = db.collection('users').order_by('points', direction=firestore.Query.DESCENDING).limit(5).stream()
                for i, u_doc in enumerate(top_users, 1):
                    ud = u_doc.to_dict()
                    
                    u_id = ud.get('id', u_doc.id)
                    u_name = ud.get('full_name', '')
                    if not u_name or u_name.strip() == "":
                        u_name = "عضو غامض"
                        
                    u_pts = ud.get('points', 0)
                    u_rank, _ = get_rank(u_pts)
                    
                    medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "▫️"
                    
                    # 🌟 التعديل السحري: التفريق بين الأدمن والمستخدم العادي 🌟
                    if int(user_id) == int(MY_CHAT_ID):
                        # إذا كان الذي يقرأ هو الإدارة (أنت): يظهر كـ رابط
                        formatted_name = f"[{u_name}](tg://user?id={u_id})"
                    else:
                        # إذا كان مستخدم عادي: يظهر كـ نص عادي عريض
                        formatted_name = f"*{u_name}*"
                    
                    lines.append(f"{medal} `{i}`. {formatted_name}\n   💎 الرصيد: `{u_pts}` نقطة | {u_rank}\n")
        except Exception as e:
            print(f"Error fetching leaderboard: {e}")
            lines.append("⚠️ جاري تحديث بيانات لوحة الشرف حالياً...")

        lines.append("━━━━━━━━━━━━━━━━━━\n💡 شارك رابط دعوتك الخاص الآن في جميع المجموعات والمنصات لتتصدر قائمة العمالقة وتحصل على جوائز شهرية حصرية!")
        text = "\n".join(lines)
        markup = types.InlineKeyboardMarkup().row(types.InlineKeyboardButton("🏠 العودة للرئيسية", callback_data="back_start"))
        bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        return
        
    # ====================================================================================
    # 🤖 المنظومة 4: مساعد التشخيص الذكي لأعطال السوفت وير (GSM Wizard)
    # ====================================================================================
    elif cd == "gsm_wizard_start":
        try: bot.answer_callback_query(call.id)
        except: pass
        markup = types.InlineKeyboardMarkup()
        markup.row(types.InlineKeyboardButton("📱 أجهزة سامسونج Samsung", callback_data="wizard_brand_samsung"))
        markup.row(types.InlineKeyboardButton("📱 أجهزة شاومي Xiaomi / Redmi", callback_data="wizard_brand_xiaomi"))
        markup.row(types.InlineKeyboardButton("🍏 أجهزة آيفون iPhone / iPad", callback_data="wizard_brand_iphone"))
        markup.row(types.InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="back_start"))
        
        bot.edit_message_text("🤖 **مساعد HMAX الذكي لتشخيص أعطال السوفت وير حَق الجوالات:**\n\nمرحباً بك يا غالي في نظام التوجيه الذكي خطوة بخطوة. سأساعدك في العثور على الأداة أو الحل المناسب لعطلك فورا!\n\n👇 **الخطوة 1: اختر ماركة هاتف الزبون المراد صيانته وعلاجه:**", user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        return

    elif cd.startswith("wizard_brand_"):
        brand = cd.replace("wizard_brand_", "")
        try: bot.answer_callback_query(call.id)
        except: pass
        
        markup = types.InlineKeyboardMarkup()
        if brand == "samsung":
            markup.row(types.InlineKeyboardButton("🔒 تخطي حساب جوجل FRP أو KG حماية حديثة", callback_data="wizard_issue_samsung_frp"))
            markup.row(types.InlineKeyboardButton("🔓 تخطي حماية وحظر حماية Bypass KNOX", callback_data="page_text_bypass_knox"))
        elif brand == "xiaomi":
            markup.row(types.InlineKeyboardButton("🔒 قفل حساب مي وتجمد البرامج Mi Account", callback_data="halab_free_redmi_mi"))
            markup.row(types.InlineKeyboardButton("📶 تفعيل نظام وصوت الـ VoLTE للـ 4G", callback_data="volte_method_1"))
        elif brand == "iphone":
            markup.row(types.InlineKeyboardButton("📡 ثبات تغطية شبكة يمن موبايل ملفات IPCC", callback_data="iphone_unlock_ipcc"))
            markup.row(types.InlineKeyboardButton("🔓 تخطي قفل وتنشيط الآيكلاود مجاناً للـ A5", callback_data="gift_icloud_a5"))
            
        markup.row(types.InlineKeyboardButton("🔙 رجوع للخطوة السابقة", callback_data="gsm_wizard_start"))
        bot.edit_message_text("🤖 **مساعد التشخيص الذكي حَق HMAX:**\n\n📐 تم رصد نوع وماركة الهاتف المستهدف بنجاح.\n\n👇 **الخطوة 2: اختر المشكلة أو العطل التقني الذي يواجهه هاتف الزبون حالياً:**", user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        return

    elif cd == "wizard_issue_samsung_frp":
        try: bot.answer_callback_query(call.id)
        except: pass
        markup = types.InlineKeyboardMarkup()
        markup.row(types.InlineKeyboardButton("🛠️ تحميل أداة AndroidUtility v200 العملاقة فورا", callback_data="link_tools_android_utility"))
        markup.row(types.InlineKeyboardButton("🔙 رجوع لمساعد التشخيص", callback_data="gsm_wizard_start"))
        bot.edit_message_text("🤖 **نتيجة التشخيص الذكي القاطع للمساعد الآلي حَق البوت:**\n\n💡 **العطل المكتشف:** قفل حماية حساب جوجل FRP أو معالج Exynos لسامسونج لعام 2026.\n\n🛠️ **الأداة المقترحة والموصى بها حَقك:**\nتعتبر أداة **AndroidUtility v200** الحصرية هي الخيار المجاني المضمون مية بالمية لفتح البورت وتفعيل ثغرة الـ ADB بلمحة بصر فورا.\n\n👇 اضغط على زر السيرفر أدناه للانتقال للتحميل المباشر والخطوات الشاملة مجاناً:", user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        return

    # ====================================================================================
    # 📈 المنظومة 5: نظام التتبع الفوري والمباشر للطلبات (Live Order Tracker)
    # ====================================================================================
    elif cd == "page_my_requests":
        try: bot.answer_callback_query(call.id)
        except: pass
        
        lines = ["📈 **سجل تتبع طلبات الصيانة والشرائح الحية حَقك:**\n━━━━━━━━━━━━━━━━━━\n"]
        has_requests = False
        try:
            if db:
                user_reqs = db.collection('user_requests').where('user_id', '==', user_id).order_by('request_date', direction=firestore.Query.DESCENDING).limit(5).stream()
                for i, r_doc in enumerate(user_reqs, 1):
                    has_requests = True
                    rd = r_doc.to_dict()
                    r_text = rd.get('request_text', 'طلب صيانة مخصص')
                    r_date = rd.get('request_date', 'اليوم')
                    
                    r_status = rd.get('status', 'قيد المراجعة ⏳')
                    status_emoji = "✅ مكتمل" if "مكتمل" in r_status or "نجاح" in r_status else "⏳ قيد المراجعة" if "مراجعة" in r_status else "🛠️ جاري العمل"
                    
                    lines.append(f"`{i:02d}.` {r_text}\n     🕐 تاريخه: `{r_date}` | 📊 حالته: **{status_emoji}**\n")
        except Exception as e:
            print(f"Error in Live Tracker pull: {e}")
            
        if not has_requests:
            lines.append("ℹ️ **لا توجد لديك أي طلبات تفعيل سيرفرات أو سحب ملفات حالياً.**\nابدأ بطلب أداة أو ترخيص لتظهر إحصائياتها الحية هنا فورا!")
            
        lines.append("━━━━━━━━━━━━━━━━━━\n💡 يتم تحديث حالة طلباتك برمجياً من السيرفر مباشرة لايف بمجرد مراجعة م/ هيثم ماكس للعملية.")
        text = "\n".join(lines)
        
        markup = types.InlineKeyboardMarkup().row(types.InlineKeyboardButton("🏠 العودة للرئيسية", callback_data="back_start"))
        bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        return


    # ===== 💡 قسم تجارب ناجحة (إشعار منبثق + عرض القائمة) =====
    elif cd == "success_exp":
        alert_text = "عزيزي المبرمج، إذا كان لديك تجارب يستفيد منها المبرمجون (قديمة أو جديدة) وتريد نشرها باسمك في بوت هيثم ماكس، أرسلها بالخاص للإدارة وسيتم نشرها لتعم الفائدة! 🚀"
        try:
            # إظهار الرسالة المنبثقة
            bot.answer_callback_query(call.id, text=alert_text, show_alert=True)
        except Exception as e:
            print(f"❌ خطأ في إشعار التجارب الناجحة: {e}")

        display_text = (
            "💡 **قسم التجارب الناجحة والمضمونة:**\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "اختر التجربة أو الحل المناسب من القائمة أدناه:"
        )

        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("📱 حل تدمير النظام REDMI 12C (ماجد المسوري)", callback_data="exp_redmi_12c"),
            types.InlineKeyboardButton("📱 حل موت MOTO G56 5G بعد FRP (محمود الدخاخني)", callback_data="exp_moto_g56"),
            types.InlineKeyboardButton("🔙 رجوع لقسم الحلول", callback_data="back_solutions_menu")  # ضع هنا callback_data الخاص بقائمة الحلول السابقة
        )

        try:
            bot.edit_message_text(
                display_text, 
                call.message.chat.id, call.message.message_id, 
                reply_markup=markup, parse_mode="Markdown"
            )
        except Exception as e:
            print(f"❌ خطأ في فتح قائمة التجارب الناجحة: {e}")
        return

    # ===== 📱 تفاصيل تجربة REDMI 12C =====
    elif cd == "exp_redmi_12c":
        try: bot.answer_callback_query(call.id)
        except: pass
        
        display_text = (
            "📱 **حل مشكلة تدمير النظام لهاتف REDMI 12C**\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "📌 **منقول عن الأخ/ ماجد المسوري:**\n\n"
            "إذا واجهتك مشكلة في هاتف **REDMI 12C**:\n"
            "• ظهور رسالة: *(تم تدمير النظام / System has been destroyed)*.\n"
            "• الجهاز على تحديث HyperOS.\n"
            "• محاولة فتح البوتلودر عبر أي أداة لا تنجح لعدم توفر الدعم.\n\n"
            "💡 **الحل:**\n"
            "قم بتحميل الفلاشة المناسبة من الرابط أدناه وتفليشها، وسيعمل الجهاز بشكل طبيعي وبدون مشاكل.\n"
            "━━━━━━━━━━━━━━━━━━"
        )
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🖼️ مشاهدة صور التجربة", url="https://t.me/haithamMax1/1088"),
            types.InlineKeyboardButton("📥 تحميل الفلاشة المناسبة", url="https://mifirm.net/download/9275?fbclid=IwdGRleAUYE7ZwZG9mBWZkaWQWUOlTHvOrcZqS2pQVVigxuRVzgUDbMmV4dG4DYWVtAjExAHNydGMGYXBwX2lkCjY2Mjg1NjgzNzkAAR5IcHdOWz84CEwwBsONMfxjaOgabaDcxgMjW7GlFiwOIEgIDhnoTZQOLdDInw_aem_bGXeXQYzE6Z6xHQdN_TwIQ"),
            types.InlineKeyboardButton("🔙 العودة للتجارب الناجحة", callback_data="success_exp")
        )
        
        try:
            bot.edit_message_text(
                display_text, 
                call.message.chat.id, call.message.message_id, 
                reply_markup=markup, parse_mode="Markdown"
            )
        except Exception as e:
            print(f"❌ خطأ في عرض تجربة Redmi 12C: {e}")
        return

    # 2️⃣ كود الاستجابة عند الضغط على الزر (داخل دالة callback_query):
    # ===== 📱 تفاصيل تجربة MOTO G56 5G =====
    elif cd == "exp_moto_g56":
        try: bot.answer_callback_query(call.id)
        except: pass
        
        # وضع رابط التيليجرام داخل كود مخفي في البداية مع تفعيل المعاينة لإظهار الصورة مباشرة داخل البوت
        display_text = (
            "[​​](https://t.me/haithamMax1/1090)"
            "📱 **حل موت هاتف MOTO G56 5G بعد عملية FRP**\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "🌹 **شكراً للأخ / Mahmoud Eldakhakhny**\n\n"
            "📌 **تشخيص العطل:**\n"
            "الجهاز فصل (ريح) بعد عملية تخطي FRP على أداة TSM من وضع Fastboot وأصبح يقرأ بورت فقط.\n\n"
            "⚙️ **خطوات الحل (إذا الجهاز يقرأ بورت):**\n"
            "1. افتح أداة **AMT**.\n"
            "2. اختر موديل **Redmi Note 14 5G**.\n"
            "3. ادخل على **Partition Manager**.\n"
            "4. حدد البارتشنات: `lk_a` و `lk_b`.\n"
            "5. اكتب فيهما الملف المرفق (خاص بنظام Android 16).\n\n"
            "🔌 **إذا كان الجهاز لا يقرأ بورت:**\n"
            "• يلزم توصيل الجهاز عبر **JTAG** وتمرير نفس الملف.\n"
            "• متوفر بالأسفل رابط الفلاشة الكاملة المخصصة لأندرويد 16.\n"
            "━━━━━━━━━━━━━━━━━━"
        )
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("📥 تحميل ملف lk (إذا كان يقرأ بورت)", url="https://drive.google.com/file/d/1Y_2SgV1LVr0hyfFjLycBHc1Ywa1P6YIt/view?usp=sharing"),
            types.InlineKeyboardButton("📥 تحميل الفلاشة الكاملة أندرويد 16 (JTAG)", url="https://drive.google.com/file/d/1jord8coH93pqrtyQ6FxONIdZG93c8Y0o/view?usp=sharing"),
            types.InlineKeyboardButton("🖼️ فتح المنشور الأصلي في تيليجرام", url="https://t.me/haithamMax1/1090"),
            types.InlineKeyboardButton("🔙 العودة للتجارب الناجحة", callback_data="success_exp")
        )
        
        try:
            bot.edit_message_text(
                display_text, 
                call.message.chat.id, call.message.message_id, 
                reply_markup=markup, parse_mode="Markdown",
                disable_web_page_preview=False  # ضروري لإظهار معاينة الصورة أعلى النص
            )
        except Exception as e:
            print(f"❌ خطأ في عرض تجربة Moto G56: {e}")
        return


    
   # ===== 📢 قسم الإعلانات المدفوعة (سوق المبرمجين) =====
    elif cd == "paid_ads_menu":
        try: bot.answer_callback_query(call.id)
        except: pass
        
        ad_text = (
            "📢 **سوق المبرمجين (أعلن معنا):**\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "للإعلان عن أدواتك أو ملفاتك المدفوعة، يجب إرسال فيديو إثبات أو نسخة تجريبية للإدارة لفحصها أولاً لضمان الجودة للعملاء.\n\n"
            "✅ **بعد الموافقة:**\n"
            "يتم دفع رسوم الإعلان، وسنقوم بنشر إعلانك لآلاف المشتركين في البوت.\n\n"
            "💬 **النتيجة:**\n"
            "سيتواصل معك العملاء مباشرة لتبيع طريقتك، أو ملفك، أو أي أداة تريدها بكل سهولة وموثوقية!\n"
            "━━━━━━━━━━━━━━━━━━"
        )
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        
        # 👇 إضافة زر توصيلات الآيفون هنا 👇
        markup.add(types.InlineKeyboardButton("📱 توصيلات تخطي الآيفون", callback_data="iphone_cables"))
        
        # الأزرار الأساسية للقسم
        markup.add(
            types.InlineKeyboardButton("💬 مراسلة الإدارة لطلب نشر إعلانك", url=f"tg://user?id={MY_CHAT_ID}"),
            types.InlineKeyboardButton("🏠 العودة للرئيسية", callback_data="back_start")
        )
        
        try:
            bot.edit_message_text(
                ad_text,
                call.message.chat.id, call.message.message_id, 
                reply_markup=markup, parse_mode="Markdown"
            )
        except Exception as e:
            print(f"❌ خطأ في فتح قسم الإعلانات: {e}")
        return

    # ===== 📱 قسم توصيلات تخطي الآيفون =====
    elif cd == "iphone_cables": 
        try: bot.answer_callback_query(call.id)
        except: pass
        
        display_text = (
            "📣 **متوفر لدينا جميع أنواع توصيلات تخطي الآيفون**\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "📦 **الأنواع والأسعار:**\n"
            "1️⃣ **RP2354A** | السعر: 45 دولار\n"
            "2️⃣ **B4 PICO** | السعر: 40 دولار\n"
            "3️⃣ **Pico 2** | السعر: 35 دولار\n"
            "4️⃣ **P2350** | السعر: 30 دولار\n\n"
            "⚡❌🔴⭕️\n"
            "**اطلب الآن.. الكمية محدودة!**\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "🆕 **سجل التغييرات:**\n"
            "تمت إضافة دعم للأنظمة التالية:\n"
            "• iOS 18\n"
            "• iOS 26\n"
            "• iOS 27\n\n"
            "🚀 **مميزات البرنامج:**\n"
            "⚡ تجاوز قفل الشاشة ورمز المرور لأجهزة iPhone و iPad المزودة بشريحة A12/A13 (مع وجود إشارة).\n"
            "⚡ استخراج معلومات المالك. 😃\n"
            "⚡ تجاوز شاشة الترحيب لأجهزة iPhone و iPad المزودة بشريحة A12/A13 (بدون وجود إشارة).\n\n"
            "📱 **الطرازات المدعومة:**\n"
            "• iPhone XS / XS Max / XR\n"
            "• iPhone 11 / 11 Pro / 11 Pro Max\n"
            "• iPhone SE (الجيل الثاني)\n"
            "• iPad Air (الجيل الثالث)\n"
            "• iPad mini (الجيل الخامس)\n"
            "• iPad (الجيل الثامن)\n"
        )
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🖼️ مشاهدة صور التوصيلات", url="https://t.me/haithamMax1/1061"),
            types.InlineKeyboardButton("🛒 لطلب الكمية (مراسلة الإدارة)", url=f"tg://user?id={MY_CHAT_ID}"),
            types.InlineKeyboardButton("🔙 العودة لقسم الإعلانات", callback_data="paid_ads_menu") # تم تعديل زر العودة هنا
        )
        
        try:
            bot.edit_message_text(
                display_text, 
                call.message.chat.id, call.message.message_id, 
                reply_markup=markup, parse_mode="Markdown"
            )
        except Exception as e:
            print(f"❌ خطأ في فتح قسم توصيلات الايفون: {e}")
        return
    

    elif cd == "number_detector":
        # 1. إنهاء حالة التحميل فوراً
        bot.answer_callback_query(call.id, "جاري فتح كاشف الأرقام...")
        
        # 2. تجهيز الرابط والأزرار
        bot_link = "https://t.me/Yemennumber_bot"
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("👉 اضغط للذهاب للبوت", url=bot_link))
        markup.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="gift_section"))
        
        # 3. تعديل الرسالة باستخدام متغيرات call المباشرة والأمنة (بدون ماركداون معقد لتجنب المشاكل)
        try:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=f"🔍 بوت كاشف الأرقام اليمني\n\nيمكنك استخدامه عبر الرابط التالي:\n{bot_link}",
                reply_markup=markup
            )
        except Exception as e:
            # إذا حدث أي خطأ برميجي، سيقوم البوت بطباعته في الـ Logs لتعرفه
            print(f"Error in number_detector: {e}")

    elif cd == "page_gift_samsung_exynos":
        track_tool("FRP SAMSUNG All Model EXYNOS", user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton("⬇️ تحميل سكريبت التخطي", url="https://www.mediafire.com/file/szt3rhif4sac9yc/FrpSamsung_2026.zip/file"),
                   types.InlineKeyboardButton("🔙 رجوع", callback_data="gift_section"))
        localized_desc = hmaxi18n.translate_static_content(
            "samsung_exynos_gift", SAMSUNG_EXYNOS_GIFT_DESC, hmaxi18n.get_language(user_id)
        )
        bot.edit_message_text(localized_desc, user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif cd == "iphone_free_service":
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🔗 1. تحميل أداة S-unlocker", url="https://mega.nz/folder/zcJyzKJB#Xnw5ZTRM_U-Yv0VdpJUkLQ"),
            types.InlineKeyboardButton("📱 2. iPHONE 5s TO X (iOS 14-17)", callback_data="req_series_1"),
            types.InlineKeyboardButton("🚀 3. XR TO 17 PRO MAX (iOS 18.6-26.1)", callback_data="req_series_2"),
            types.InlineKeyboardButton("🔙 رجوع", callback_data="gift_section")
        )
        
        # كود نصي نظيف ومحمي بأسلوب السطر الواحد لتجنب تكسير كيبورد الجوال
        text = "🚀 **بشرى سارة لجميع مستخدمي الآيفون والآيباد!** 🎉\n\nيسر فريقنا أن يعلن عن توفر خدمة تخطي أجهزة الآيفون والآيباد مجاناً بالكامل وبدون أي تكلفة عليك.\n\n🚀 **تفاصيل الخدمة:**\n1️⃣ iPhone 5s to X: iOS 14 - 17\n2️⃣ XR to 17 Pro Max: iOS 18.6 - 26.1\n\n✅ **الخطوات:**\n1. حمل الأداة من الزر الأول.\n2. استخرج السيريال.\n3. اختر نوع جهازك من الأزرار لطلب الرفع."
        
        bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif cd == "req_series_1":
        request_s_unlocker(call.message, "iPhone 5s to X")
        
    elif cd == "req_series_2":
        request_s_unlocker(call.message, "XR to 17 Pro Max")

    # ================= 🆕 معالج لوحة أداة تخطي الآيكلاود A5 (القائمة الفرعية المحدثة) =================
    elif cd == "gift_icloud_a5":
        track_tool("قائمة أداة تخطي الآيكلاود A5", user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("📋 القسم الأول: (بدون كلمة سر)", callback_data="gift_a5_part1"),
            types.InlineKeyboardButton("🔐 القسم الثاني: (مع كلمة السر 1988)", callback_data="gift_a5_part2"),
            types.InlineKeyboardButton("📂 البرنامج المضمون لتخطي", callback_data="gift_a5_guaranteed"), # 🌟 الخيار الثالث الجديد
            types.InlineKeyboardButton("🔙 رجوع لقسم الهدايا", callback_data="gift_section")
        )
        bot.edit_message_text(
            "💢 **أداة تخطي الآيكلاود مجاناً لمعالجات A5 (تجريبي):**\n\n"
            "تم تنظيم الأداة والشروحات والملفات المضمونة لفتح الآيبادات لتسهيل عملية التخطي بنجاح.\n\n"
            "💡 **اختر القسم البرمجي الذي تود عرضه أدناه للبدء:**",
            user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown"
        )
        return

    # 📋 عرض تفاصيل القسم الأول
    elif cd == "gift_a5_part1":
        track_tool("آيكلاود A5 - القسم الأول", user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("📥 اضغط هنا للتحميل من التيلجرام", url="https://t.me/gaddtech/1572"),
            types.InlineKeyboardButton("🎬 لمشاهدة شرح الطريقة على يوتيوب", url="https://youtu.be/Qq1WLY8Axx8"),
            types.InlineKeyboardButton("🔙 رجوع لخيارات الأقسام", callback_data="gift_icloud_a5")
        )
        
        display_text = (
            "📋 **أداة تخطي الآيكلاود لمعالجات A5 - القسم الأول:**\n\n"
            "أداة جديدة ومميزة لتخطي الآيكلاود للأجهزة القديمة بضغطة زر وبدون تعقيد.\n\n"
            "⚙️ **A5 Device Bypass Tool iCloud**\n\n"
            "📌 **أبرز ميزات ووظائف الأداة:**\n"
            "• تدعم جميع الهواتف والآيبادات القديمة ذات معالجات A5.\n"
            "• تعمل بالكامل **بدون جيلبريك** لتوفر عليك عناء البحث عن ثغرات.\n"
            "• تدعم أجهزة كلاسيكية هامة مثل: `iPad 2` و `iPad Mini 1` و `iPhone 5` و `iPhone 4` وغيرها من الموديلات القديمة العالقة.\n"
            "━━━━━━━━━━━━━━━━━\n"
            "📥 للتحميل المباشر ومتابعة خطوات الشرح بالفيديو، اضغط أدناه:"
        )
        bot.edit_message_text(display_text, user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        return

    # 🔐 عرض تفاصيل القسم الثاني (المزود بكلمة السر 1988)
    elif cd == "gift_a5_part2":
        track_tool("آيكلاود A5 - القسم الثاني", user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("📥 اضغط هنا للتحميل من التيلجرام", url="https://t.me/gaddtech/1572"),
            types.InlineKeyboardButton("🎬 لمشاهدة شرح الطريقة على يوتيوب", url="https://youtu.be/Qq1WLY8Axx8"),
            types.InlineKeyboardButton("🔙 رجوع لخيارات الأقسام", callback_data="gift_icloud_a5")
        )
        
        display_text = (
            "🔐 **أداة تخطي الآيكلاود لمعالجات A5 - القسم الثاني:**\n\n"
            "أداة جديدة ومميزة لتخطي الآيكلاود للأجهزة القديمة بضغطة زر وبدون تعقيد.\n\n"
            "⚙️ **A5 Device Bypass Tool iCloud**\n\n"
            "📌 **أبرز ميزات ووظائف الأداة:**\n"
            "• تدعم جميع الهواتف والآيبادات القديمة ذات معالجات A5.\n"
            "• تعمل بالكامل **بدون جيلبريك** لتوفر عليك عناء البحث عن ثغرات.\n"
            "• تدعم أجهزة كلاسيكية هامة مثل: `iPad 2` و `iPad Mini 1` و `iPhone 5` و `iPhone 4` وغيرها من الموديلات القديمة العالقة.\n\n"
            "🔐 **كلمة سر فك ضغط الملف:** `1988`\n"
            "━━━━━━━━━━━━━━━━━\n"
            "📥 للتحميل المباشر ومتابعة خطوات الشرح بالفيديو، اضغط أدناه:"
        )
        bot.edit_message_text(display_text, user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        return

    # 📂 ================= 🆕 معالج خيار البرنامج المضمون لتخطي الآيبلدات =================
    elif cd == "gift_a5_guaranteed":
        track_tool("البرنامج المضمون لتخطي الآيكلاود", user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("📥 فتح مجلد التحميل المضمون من ميديا فاير", url="https://www.mediafire.com/folder/vgdqfdik8dg86/فتح_ايكلود_الايبادات"),
            types.InlineKeyboardButton("🔙 رجوع لخيارات الأقسام", callback_data="gift_icloud_a5")
        )
        
        display_text = (
            "📂 **البرنامج المضمون لفتح وتخطي آيكلاود الآيبادات:**\n\n"
            "إليك المجلد السيرفري الشامل والمضمون الذي يحتوي على كافة البرامج والأدوات اللازمة لإتمام عملية فتح وتخطي حسابات الآيكلاود لأجهزة الآيباد والـ A5 القديمة بنجاح وبدون مشاكل تعليق.\n\n"
            "━━━━━━━━━━━━━━━━━\n"
            "📥 لتصفح المجلد وتحميل البرامج مباشرة عبر ميديا فاير، اضغط أدناه:"
        )
        bot.edit_message_text(display_text, user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        return

    elif cd == "gift_fmi_off":
        try: bot.answer_callback_query(call.id)
        except: pass
        
        # النص الخاص بالهدية متضمناً الرابط والتنسيق المطلوب
        fmi_text = (
            "🍏🍏🍏🍏🍏\n"
            "*FMI OFF - Open Menu*\n"
            "*New Generation 2026🔥*\n"
            "🆓\n"
            "• No Need Shortcut\n"
            "• No Need PC\n"
            "• Remove Instant\n"
            "• Support Safari / Firefox / Chrome\n\n"
            "*FMI Page :*\n"
            "https://fmip.indofind.my.id/2026/\n\n"
            "_Send your code to reseller or submit on web sourceunlock.com to make findmy off._"
        )
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        # زر يوجه المستخدم مباشرة لمشاهدة فيديو الشرح
        markup.add(
            types.InlineKeyboardButton("▶️ فيديو الشرح (Video Guide)", url="https://t.me/haithamMax1/974"),
            types.InlineKeyboardButton("🏠 العودة للرئيسية", callback_data="back_start")
        )
        
        try:
            # disable_web_page_preview=True لمنع تليجرام من إظهار صورة كبيرة للموقع تشوه شكل النص
            bot.edit_message_text(
                fmi_text,
                call.message.chat.id, call.message.message_id, 
                reply_markup=markup, parse_mode="Markdown", disable_web_page_preview=True
            )
        except Exception as e:
            print(f"❌ خطأ في قسم هدية FMI: {e}")
        return

# ================= 🆕 معالج قسم الحلول المنقولة والمضمونة لمشاكل الهواتف الرئيسي =================
   
    # ==========================================
    # 📦 قسم الحلول المنقولة والمضمونة (الرئيسي)
    # ==========================================
    elif cd == "phone_solutions_main":
        try: bot.answer_callback_query(call.id)
        except: pass
        if 'track_tool' in globals(): track_tool("قسم الحلول المضمونة", user_id)
        
        markup = types.InlineKeyboardMarkup()
        markup.row(types.InlineKeyboardButton("📺 FRP FREE YOUTUBE", callback_data="sol_youtube"))
        markup.row(types.InlineKeyboardButton("📝 شرح نصي", callback_data="sol_text"))
        markup.row(types.InlineKeyboardButton("🆓 فتح شفرات مجاناً 🆓", callback_data="sol_free_unlock"))
        markup.row(types.InlineKeyboardButton("📁 ملفات", callback_data="sol_files"))
        markup.row(types.InlineKeyboardButton("💡 تجارب ناجحة", callback_data="success_exp"))
        markup.row(
            types.InlineKeyboardButton("📶 تفعيل الفولتي", callback_data="sol_volte"),
            types.InlineKeyboardButton("✨ لمسات عبدالملك", callback_data="sol_abdulmalik")
        )
        markup.row(
            types.InlineKeyboardButton("👑 لمسات رشيد مدغمر 👑", callback_data="sol_rasheed")
        )
        markup.row(
            types.InlineKeyboardButton("📦 قسم تطبيقات APK", callback_data="sol_apk")
        )
        # 🌟 الزر الجديد الخاص بشروحاتك
        markup.row(
            types.InlineKeyboardButton("💡 شروحات هيثم ماكس", callback_data="sol_haitham_max")
        )
        markup.row(types.InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="back_start"))
        
        display_text = (
            "📦 **قسم الحلول المنقولة والمضمونة لمشاكل الهواتف:**\n\n"
            "مرحباً بك في القسم المخصص لعرض خلاصة الحلول البرمجية والتقنية المجربة والمضمونة بنسبة 100% لحل أعقد مشاكل الهواتف الذكية.\n\n"
            "💡 **اختر نوع الشرح أو الخدمة التي تريد تصفحها بالأسفل:**"
        )
        bot.edit_message_text(display_text, user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        return

    # ==========================================
    # 💡 قسم شروحات هيثم ماكس الحصرية (YouTube)
    # ==========================================
    elif cd == "sol_haitham_max":
        try: bot.answer_callback_query(call.id)
        except: pass
        if 'track_tool' in globals(): track_tool("دخول قسم شروحات هيثم ماكس", user_id)
        
        # وضعنا الأزرار تحت بعضها (زر واحد في كل صف) لكي تظهر النصوص بشكل واضح
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("📺 FRP LT Mobile | TSM PRO", url="https://youtu.be/b45iEOYj8BE"),
            types.InlineKeyboardButton("📺 FRP Moto G05 (XT2523-4)", url="https://youtu.be/M153OfllQtU"),
            types.InlineKeyboardButton("📺 FRP Moto XT2515-2 | TSM PRO", url="https://youtu.be/PLY4u9ANCpg"),
            types.InlineKeyboardButton("📺 FRP Benco AE9240 | TSM PRO", url="https://youtu.be/ingczBKUFGc"),
            types.InlineKeyboardButton("📺 عرض شاشة الآيفون للكمبيوتر (بدون كابل)", url="https://youtu.be/Y3spa6koDnI"),
            types.InlineKeyboardButton("📺 Root & VoLTE Moto G Power 2025", url="https://youtu.be/ut2CB7t3A-4"),
            types.InlineKeyboardButton("📺 FRP Tecno Spark Go 2 (KM4)", url="https://youtu.be/t9roIUgeu1Y"),
            types.InlineKeyboardButton("📺 FRP Moto G 5G 2025 FastBoot", url="https://youtu.be/w-HN_7ASnCM"),
            types.InlineKeyboardButton("📺 FRP Moto G06 One Click | TSM", url="https://youtu.be/Chfxjh1Byd8"),
            types.InlineKeyboardButton("📺 Root & VoLTE Moto G 2025 (Android 16)", url="https://youtu.be/Q06v_VY5yT8"),
            types.InlineKeyboardButton("📺 FRP Moto G35 (Android 15)", url="https://youtu.be/4kBRW5ZK7do"),
            types.InlineKeyboardButton("📺 FRP Moto E15 (Android 14)", url="https://youtu.be/ToE5Ke2LzEk"),
            types.InlineKeyboardButton("🔙 رجوع لقسم الحلول", callback_data="phone_solutions_main")
        )
        
        display_text = (
            "💡 **شروحات هيثم ماكس الحصرية:**\n\n"
            "مرحباً بك في قسم الشروحات المرئية. قمنا بتجميع أفضل الفيديوهات والحلول العملية الحصرية لتسهيل عملك البرمجي، خصوصاً مع أداة TSM PRO.\n\n"
            "👇 **اختر الشرح الذي تريد مشاهدته مباشرة على يوتيوب:**"
        )
        
        bot.edit_message_text(
            display_text, user_id, call.message.message_id, 
            reply_markup=markup, parse_mode="Markdown"
        )
        return

    # ==========================================
    # 📦 قسم تطبيقات الـ APK وتفريعاته
    # ==========================================
    elif cd == "sol_apk":
        try: bot.answer_callback_query(call.id)
        except: pass
        if 'track_tool' in globals(): track_tool("دخول قسم APK", user_id)
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🛠️ إصلاح تطبيق Samsung Messages الأصلي", callback_data="sol_apk_samsung_msg"),
            types.InlineKeyboardButton("🔙 رجوع لقسم الحلول الرئيسي", callback_data="phone_solutions_main")
        )
        bot.edit_message_text(
            "📦 **قسم تطبيقات وحلول الـ APK:**\n\nاختر التطبيق أو الحل المطلوب من القائمة أدناه:",
            user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown"
        )
        return

    # 🌟 معالج صفحة تفاصيل إصلاح رسائل سامسونج
    elif cd == "sol_apk_samsung_msg":
        try: bot.answer_callback_query(call.id)
        except: pass
        if 'track_tool' in globals(): track_tool("شرح إصلاح Samsung Messages", user_id)
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("📥 رابط التحميل (mega)", url="https://mega.nz/file/chQQmJCR#AsBHKct4UoxIOSKB7H-_vcgijpgh1kmMHzO8IJ8o6xg"),
            types.InlineKeyboardButton("🔗 رابط المنشور السابق للاطلاع", url="https://shorturl.at/fFiTX"),
            types.InlineKeyboardButton("🔙 رجوع لقسم APK", callback_data="sol_apk")
        )
        
        display_text = (
            "🛠️ **إصلاح تطبيق Samsung Messages الأصلي**\n\n"
            "تحديثاً للمنشور السابق بخصوص تطبيق رسائل سامسونج وسكربت `Samsung Messages Restorer`.\n"
            "خلال الفترة السابقة كنت أحاول البحث عن حلول أكثر للموضوع حتى نواكب حل هذه المشكلة إلى حين نصل لحل نهائي...\n\n"
            "⚠️ **طبيعة المشكلة:**\n"
            "ظهرت مشكلة أن التطبيق ممكن يجلس أيام أو أسابيع معينة وبعدين للأسف يتحدث، لأن موضوع السكربت السابق كان حل مؤقت، وفعلاً بيصير تحديث صامت للتطبيق.\n\n"
            "✅ **التحديثات والميزات الجديدة:**\n"
            "عملت تحديث للسكربت وأضفت فيه ميزات (حلول مؤقتة لحين الحل النهائي، وممكن يمشي معانا فترة حلوة):\n"
            "1️⃣ حظر التحديثات التلقائية تماماً سواء بيحدث من سيرفر سامسونج مباشرة عبر التطبيق أو من خلال `Galaxy Store`.\n"
            "2️⃣ إضافة التحقق من تطبيق الرسائل خلال العملية وترشيح وتحميل (نسختين APK) متوافقة تماماً:\n"
            "   • واحدة لإصدار أندرويد (15 - 16).\n"
            "   • والثانية لأندرويد (10 إلى 14).\n"
            "3️⃣ إعادة تثبيته كتطبيق رسمي وتحديث بشكل تام وبدون أي مشاكل.\n\n"
            "💡 **خبر تقني سار:**\n"
            "وصلني جهاز S25 أمريكي U بأحدث إصدار، استخدم السكربت وما نفع معه، فدخلت أشوف إيش الخلل من الأوامر فاكتشفت أن تطبيق رسائل سامسونج (غير موجود أصلاً)، بمعنى أن أمر `uninstall` حذف التطبيق بشكل نهائي تماماً!\n"
            "وهذا يعني أن في تحديثات لسامسونج خلت التطبيق تطبيق عادي وممكن تكون نقلته من `system/priv-app/` إلى `/product/app` أو `/system/app`.\n\n"
            "إذا أصبح التطبيق `Pre-installed App` فهذا يعني أن أي شخص يقدر يحذفه ويثبت أقدم نسخة تناسب הـ API الخاص فيه وينتهي نهائياً من هذه المشكلة.\n\n"
            "وإن شاء الله رح نواصل البحث في الحلول لحين نجد حل نهائي، خاصة أن سامسونج لها أجهزة تحت بلدان (هونج كونج) لا توجد فيها خدمات جوجل تماماً، يعني استمرار تطبيق رسائل سامسونج الرسمي.\n\n"
            "━━━━━━━━━━━━━━━━━\n"
            "👇 **لتحميل السكربت المحدث، اضغط أدناه:**"
        )
        
        bot.edit_message_text(
            display_text, user_id, call.message.message_id, 
            reply_markup=markup, parse_mode="Markdown"
        )
        return

# 🧩 معالج استقبال خانات المبدعين في القسم الرئيسي (تم فصل عبدالملك العشاري)
    elif cd == "sol_abdulmalik":
        track_tool("قسم لمسات المبدع عبدالملك العشاري", user_id)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙 رجوع لقسم الحلول", callback_data="phone_solutions_main"))
        bot.edit_message_text(
            "📥 **قسم لمسات المبدع عبدالملك العشاري مجاناً:**\n\n⏳ **قريباً...**\n\nهذا القسم قيد التجهيز والرفع حالياً، وسيتم تزويده بأحدث الطرق والملفات الحصرية والمضمونة مجاناً فوراً! 😍🔥",
            user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown"
        )
        return

    # 📶 معالج لوحة قسم تفعيل الفولتي الشامل للـ 6 شروحات الحصرية (محدث تلقائياً) 📶
    elif cd == "sol_volte":
        bot.answer_callback_query(call.id)
        track_tool("قسم تفعيل الفولتي", user_id)
        markup = types.InlineKeyboardMarkup()
        
        # تنظيم الـ 6 أزرار بشكل طولي عريض لظهور العناوين كاملة وبشكل منسق جداً
        markup.row(types.InlineKeyboardButton("📱 تفعيل VoLTE لأجهزة Xiaomi و Redmi", callback_data="volte_method_1"))
        markup.row(types.InlineKeyboardButton("📲 تشغيل الفولتي لهواتف Samsung الحديثة", callback_data="volte_method_2"))
        markup.row(types.InlineKeyboardButton("📶 تفعيل VoLTE لأجهزة OnePlus و Pixel", callback_data="volte_method_3"))
        markup.row(types.InlineKeyboardButton("🔥 حل مشكلة اختفاء الـ VoLTE بعد التحديث", callback_data="volte_method_4"))
        markup.row(types.InlineKeyboardButton("⚙️ ضبط الفولتي وإظهار أيقونة 4G/5G المفقودة", callback_data="volte_method_5"))
        markup.row(types.InlineKeyboardButton("🌐 تفعيل VoLTE لجميع معالجات MediaTek (MTK)", callback_data="volte_method_6"))
        
        markup.row(types.InlineKeyboardButton("🔙 رجوع لقسم الحلول الرئيسي", callback_data="phone_solutions_main"))
        
        bot.edit_message_text(
            text="📶 **قسم تفعيل خدمات الفولتي (VoLTE) مجاناً:**\n\nمرحباً بك في القسم المخصص لحلول وشروحات تفعيل نظام الـ VoLTE لشبكة يمن موبايل ومختلف الشبكات العالمية لأحدث الأجهزة الذكية.\n\n💡 **اختر الموديل أو طريقة الشرح المطلوبة أدناه لعرض تفاصيلها المباشرة:**",
            chat_id=user_id,
            message_id=call.message.message_id,
            reply_markup=markup,
            parse_mode="Markdown"
        )
        return

    # 1️⃣ معالج طريقة تفعيل VoLTE شاومي وريدمي
    elif cd == "volte_method_1":
        track_tool("تفعيل فولتي شاومي وريدمي", user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🎬 FRP FREE YOUTUBE", url="https://youtu.be/lddDl97pVTQ?si=kRGzEI0mNA_T5Q-P"),
            types.InlineKeyboardButton("🔙 رجوع لقسم الفولتي", callback_data="sol_volte")
        )
        display_text = (
            "📶 **تفعيل خدمة VoLTE لأجهزة Xiaomi & Redmi مجاناً:**\n\n"
            "🔥 الشرح الصحيح والمجرب لتفعيل نظام الفولتي لشبكة يمن موبايل 4G على هواتف شاومي وريدمي بوضعية الـ Diag وبدون الحاجة لعمل روت للجهاز لضمان استقرار الشبكة.\n\n"
            "🎬 اضغط على زر السيرفر أدناه لمشاهدة الخطوات بالفيديو مباشرة على يوتيوب:"
        )
        bot.edit_message_text(display_text, user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        return

    # 2️⃣ معالج طريقة تفعيل VoLTE سامسونج
    elif cd == "volte_method_2":
        track_tool("تفعيل فولتي سامسونج الحديثة", user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🎬 FRP FREE YOUTUBE", url="https://youtu.be/KUYST91E33Q?si=1x7nn5Ugv-_HP_H2"),
            types.InlineKeyboardButton("🔙 رجوع لقسم الفولتي", callback_data="sol_volte")
        )
        display_text = (
            "📶 **تشغيل الفولتي لهواتف Samsung الحديثة:**\n\n"
            "🔥 تخطي قيود الشبكة وتفعيل خدمة الـ VoLTE بثبات تام على حمايات سامسونج الجديدة لعام 2025/2026 لتشغيل البيانات والمكالمات معاً بكفاءة عالية وبدون انقطاع للتغطية.\n\n"
            "🎬 اضغط على زر السيرفر أدناه لمشاهدة الخطوات بالفيديو مباشرة على يوتيوب:"
        )
        bot.edit_message_text(display_text, user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        return

    # 3️⃣ معالج طريقة تفعيل VoLTE ون بلس وبكسل
    elif cd == "volte_method_3":
        track_tool("تفعيل فولتي ون بلس وبكسل", user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🎬 FRP FREE YOUTUBE", url="https://youtu.be/n6Xx6P5fNF0?si=dwPnxoiUGqgd67o5"),
            types.InlineKeyboardButton("🔙 رجوع لقسم الفولتي", callback_data="sol_volte")
        )
        display_text = (
            "📶 **تفعيل خدمة VoLTE لأجهزة OnePlus & Google Pixel:**\n\n"
            "🔥 الطريقة السحرية لتنشيط نظام الفولتي عبر الأكواد السرية المخفية وإعدادات النظام الداخلية لتثبيت التغطية ومنع سقوطها أثناء تصفح الإنترنت ببيانات الفورجي.\n\n"
            "🎬 اضغط على زر السيرفر أدناه لمشاهدة الخطوات بالفيديو مباشرة على يوتيوب:"
        )
        bot.edit_message_text(display_text, user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        return

    # 4️⃣ معالج حل مشكلة اختفاء الفولتي بعد التحديث
    elif cd == "volte_method_4":
        track_tool("حل مشكلة اختفاء الفولتي بعد التحديث", user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🎬 FRP FREE YOUTUBE", url="https://youtu.be/n0vHgu9zKY?si=sjRCes8KLP5bT8bK"),
            types.InlineKeyboardButton("🔙 رجوع لقسم الفولتي", callback_data="sol_volte")
        )
        display_text = (
            "📶 **حل مشكلة اختفاء الـ VoLTE بعد التحديث لشبكة يمن موبايل:**\n\n"
            "🔥 الحل النهائي والبرمجي القاطع للمشكلة الشائعة التي تواجه الفنيين عند تحديث نظام أندرويد واختفاء التغطية أو إعدادات الفولتي تلقائياً، وإعادتها للعمل بنقرة واحدة.\n\n"
            "🎬 اضغط على زر السيرفر أدناه لمشاهدة الخطوات بالفيديو مباشرة على يوتيوب:"
        )
        bot.edit_message_text(display_text, user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        return

    # 5️⃣ معالج ضبط الفولتي وإظهار أيقونة 4G/5G
    elif cd == "volte_method_5":
        track_tool("ضبط الفولتي وإظهار أيقونة الشبكة", user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🎬 FRP FREE YOUTUBE", url="https://youtu.be/CrD_StHVURo?si=_PZyp1uvbxaG89mi"),
            types.InlineKeyboardButton("🔙 رجوع لقسم الفولتي", callback_data="sol_volte")
        )
        display_text = (
            "📶 **ضبط الفولتي وإظهار أيقونة الـ 4G/5G المفقودة:**\n\n"
            "🔥 شرح مميز لكيفية تعديل ملفات الكارير وتفعيل الـ VoLTE وإظهار شعارات التغطية الحديثة على شاشة قفل وأعلى واجهة النظام عبر سكريبتات وأدوات تعريب مخصصة.\n\n"
            "🎬 اضغط على زر السيرفر أدناه لمشاهدة الخطوات بالفيديو مباشرة على يوتيوب:"
        )
        bot.edit_message_text(display_text, user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        return

    # 6️⃣ معالج تفعيل VoLTE لمعالجات MTK
    elif cd == "volte_method_6":
        track_tool("تفعيل فولتي معالجات MTK", user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🎬 FRP FREE YOUTUBE", url="https://youtu.be/bg7I-MpqkwQ?si=Ymx7aow9RyuisegC"),
            types.InlineKeyboardButton("🔙 رجوع لقسم الفولتي", callback_data="sol_volte")
        )
        display_text = (
            "📶 **تفعيل VoLTE لجميع هواتف معالجات MediaTek (MTK):**\n\n"
            "🔥 الشرح الشامل لفتح وضع الهندسة المهني (Engineer Mode) والتعديل اليدوي على شبكات الـ LTE لتفعيل ميزة المكالمات الصوتية عالية الدقة لشرائح الـ MTK الذكية.\n\n"
            "🎬 اضغط على زر السيرفر أدناه لمشاهدة الخطوات بالفيديو مباشرة على يوتيوب:"
        )
        bot.edit_message_text(display_text, user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        return
        
# 👑 معالج لوحة إبداعات وثغرات المهندس رشيد مدغمر (محدث بالـ 15 زراً الحصرية بالكامل) 👑
    elif cd == "sol_rasheed":
        bot.answer_callback_query(call.id)
        track_tool("لمسات المبدع رشيد مدغمر", user_id)
        markup = types.InlineKeyboardMarkup()
        
        # تنظيم الأزرار بشكل طولي عريض لعدم اقتطاع العناوين وظهورها بأعلى درجات التنسيق
        markup.row(types.InlineKeyboardButton("🔥 Vivo_New_Code 2026", callback_data="rash_vivo_2026"))
        markup.row(types.InlineKeyboardButton("📺 سر مخفي في هواتف TCL لضبط الـ APN", callback_data="rash_tcl_secret"))
        markup.row(types.InlineKeyboardButton("📟 رمز SPD الجديد يفتح قائمة EngineerMode", callback_data="rash_spd_code"))
        markup.row(types.InlineKeyboardButton("🛠️ كود يسمح لك بتغيير الـ IMEI", callback_data="rash_change_imei"))
        markup.row(types.InlineKeyboardButton("🍏 إظهار EngineerMode لأجهزة الآيفون كوبي", callback_data="rash_iphone_clone_eng"))
        markup.row(types.InlineKeyboardButton("📶 تغيير الـ IMEI لإظهار فولت S25 التراء بلس", callback_data="rash_s25_ultra_clone"))
        markup.row(types.InlineKeyboardButton("⚙️ تفعيل الفولتي لهواتف MTK (Cricket & AT&T)", callback_data="rash_mtk_volte"))
        
        # 🌟 الأزرار الـ 8 الجديدة المضافة تلقائياً ونظامياً 🌟
        markup.row(types.InlineKeyboardButton("📱 تفعيل VoLTE لهواتف LG (شرح سريع)", callback_data="rash_lg_volte"))
        markup.row(types.InlineKeyboardButton("🔓 حل مشكلة عدم عمل أكواد Engineer Mode", callback_data="rash_open_eng_mode"))
        markup.row(types.InlineKeyboardButton("🚀 تجاوز شاشة Activation بدون كمبيوتر", callback_data="rash_bypass_activation"))
        markup.row(types.InlineKeyboardButton("📲 فتح خيارات المطور المخفي بالايفون الكوبي", callback_data="rash_clone_developer"))
        markup.row(types.InlineKeyboardButton("🔑 استخراج رموز قفل التطبيقات عبر setedit", callback_data="rash_setedit_apps_lock"))
        markup.row(types.InlineKeyboardButton("📶 تفعيل الـ VoLTE لهواتف Revvl يدوي", callback_data="rash_revvl_volte"))
        markup.row(types.InlineKeyboardButton("📱 حل مشكلة عدم عمل VoLTE في سامسونج", callback_data="rash_samsung_volte_fix"))
        markup.row(types.InlineKeyboardButton("🌀 أسرار وفكفكة هواتف Vortex وتعديل IMEI", callback_data="rash_vortex_fix"))
        markup.row(types.InlineKeyboardButton("🛠️ فتح قائمة اصلاح الرقم التسلسلي لهواتف Coolpad", callback_data="rash_coolpad_imei"))
        markup.row(types.InlineKeyboardButton("📶 فتح قائمة تفعيل الباندات لهواتف mtk coolpad", callback_data="rash_coolpad_bands"))
        
        markup.row(types.InlineKeyboardButton("🔙 رجوع لقسم الحلول الرئيسي", callback_data="phone_solutions_main"))
        
        bot.edit_message_text(
            text="👑 **لمسات المبدع رشيد مدغمر مجاناً:**\n\nمرحباً بك في القسم الحصري للمبدع رشيد مدغمر الشامل لأقوى الأكواد والثغرات البرمجية المضمونة.\n\n💡 **اختر الخدمة أو الثغرة المطلوبة أدناه لعرض تفاصيلها والشروحات حَقها:**",
            chat_id=user_id,
            message_id=call.message.message_id,
            reply_markup=markup,
            parse_mode="Markdown"
        )
        return

    # 1️⃣ معالج ثغرة Vivo_New_Code 2026
    elif cd == "rash_vivo_2026":
        track_tool("ثغرة Vivo New Code 2026", user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🎬 الانتقال لمشاهدة الشرح على فيسبوك", url="https://www.facebook.com/share/r/1DJRE2srbS/?mibextid=wwXIfr"),
            types.InlineKeyboardButton("🔙 رجوع لقسم رشيد مدغمر", callback_data="sol_rasheed")
        )
        display_text = (
            "الكود الجديد 🔥 #Vivo_New_Code 2026 لتفعيل بورت Vcom وتخطي حساب جوجل وتشغيل الفولتي!\n\n"
            "Enable Vcom port for mtk vivo for \n"
            "Fix network\n"
            "Enable volte\n"
            "Enable Engineer mode\n\n"
            "#المبرمج_رشيدمدغمر\n"
            "#RasheedAbdalkhalik"
        )
        bot.edit_message_text(display_text, user_id, call.message.message_id, reply_markup=markup)
        return

    # 2️⃣ معالج ثغرة هواتف TCL لفتح إعدادات APN
    elif cd == "rash_tcl_secret":
        track_tool("ثغرة هواتف TCL لضبط APN", user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🎬 الانتقال لمشاهدة الشرح على فيسبوك", url="https://www.facebook.com/share/r/191MJSABCU/?mibextid=wwXIfr"),
            types.InlineKeyboardButton("🔙 رجوع لقسم رشيد مدغمر", callback_data="sol_rasheed")
        )
        display_text = (
            "سر مخفي في هواتف TCL يفتح إعدادات الcarrierو الـ APN خلال ثواني 🔥\n\n"
            "احذفوها عشان يشتغل معكم الاتصال !!!\n\n"
            "Full Guide to TCL Network Access Point Settings\n\n"
            "#المبرمج_رشيد_مدغمر\n"
            "#tcl\n"
            "#volte\n"
            "#RasheedAbdalkhalik"
        )
        bot.edit_message_text(display_text, user_id, call.message.message_id, reply_markup=markup)
        return

    # 3️⃣ معالج رمز SPD الجديد لفتح قائمة المهندس
    elif cd == "rash_spd_code":
        track_tool("رمز SPD الجديد لقائمة المهندس", user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🎬 الانتقال لمشاهدة الشرح على فيسبوك", url="https://www.facebook.com/share/r/1EZn7wQLhC/?mibextid=wwXIfr"),
            types.InlineKeyboardButton("🔙 رجوع لقسم رشيد مدغمر", callback_data="sol_rasheed")
        )
        display_text = (
            "New SPD code unlocks the engineer mode menu — may be useful for FRP and VoLTE activation\n\n"
            "#المبرمج_رشيدمدغمر\n"
            "#RasheedAbdalkhalik\n"
            "#spd #Engineermode \n"
            "#صيانة_جوالات #سوفتوير #تفليش #FRP #اصلاح_هواتف"
        )
        bot.edit_message_text(display_text, user_id, call.message.message_id, reply_markup=markup)
        return

    # 4️⃣ معالج كود تغيير IMEI للهواتف
    elif cd == "rash_change_imei":
        track_tool("كود تغيير IMEI للهواتف رشيد مدغمر", user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🎬 الانتقال لمشاهدة الشرح على فيسبوك", url="https://www.facebook.com/share/r/1CkGwXuRfw/?mibextid=wwXIfr"),
            types.InlineKeyboardButton("🔙 رجوع لقسم رشيد مدغمر", callback_data="sol_rasheed")
        )
        display_text = (
            "اللي تعرفه عن جهازك… يمكن مش كل الحقيقة 📱😏\n\n"
            "هذا كود ثاني يسمح لك بتغيير الimei في حال مااشتغل معك السابق \n"
            "M-horse phones\n"
            "What you think you know about your device… isn’t the full story!\n\n"
            "#المبرمج_رشيدمدغمر\n"
            "#صيانة_جوالات #سوفتوير #تفليش #FRP #اصلاح_هواتف\n"
            "#Rasheed_abdalkhalik"
        )
        bot.edit_message_text(display_text, user_id, call.message.message_id, reply_markup=markup)
        return

    # 5️⃣ معالج كود إظهار EngineerMode للايفون الكوبي
    elif cd == "rash_iphone_clone_eng":
        track_tool("إظهار EngineerMode للايفون الكوبي", user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🔙 رجوع لقسم رشيد مدغمر", callback_data="sol_rasheed")
        )
        display_text = (
            "كثير منكم يسأل عن كيفية الوصول لإعدادات ال Engineer Mode في هواتف الآيفون \"الكوبي\" أو الـ Clone التي تعمل بنظام أندرويد بواجهة iOS. اليوم مر عليّ جهاز من هذه النوعية، وحبيت أشارككم الكود الخاص بفتح Engineer Mode للتحكم في خصائص الشبكة مثل الvolte وغيرها مثل ، الصوت، واختبارات الهاردوير.\n\n"
            "الكود هو:\n"
            "*#*#136466331#*#*\n\n"
            "للأسف لم يسعفني الوقت لتصوير فيديو للجهاز، لكن الكود شغال ومجرب\n\n"
            "#رشيد_عبدالخالق \n"
            "#المبرمج_رشيدمدغمر \n"
            "#iPhoneClone #EngineerMode #صيانة_موبايل #تطوير_أندرويد"
        )
        bot.edit_message_text(display_text, user_id, call.message.message_id, reply_markup=markup)
        return

    # 6️⃣ معالج تغيير IMEI لجوال S25 Ultra بلس كوبي لتفعيل VoLTE
    elif cd == "rash_s25_ultra_clone":
        track_tool("تغيير IMEI لجوال S25 Ultra كوبي", user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🎬 الانتقال لمشاهدة الشرح على فيسبوك", url="https://www.facebook.com/share/r/1BQS2DaRSb/?mibextid=wwXIfr"),
            types.InlineKeyboardButton("🔙 رجوع لقسم رشيد مدغمر", callback_data="sol_rasheed")
        )
        display_text = (
            "#تغيير الimei ليعمل #الفولتي على هاتف S25 Ultra plus Clone(كوبي)\n"
            "#Change_IMEI for #S25 Ultra Clone (SPD)\n\n"
            "تم ضبط الهاتف عبر port الSpd ولكن لم يعمل وتم عمل فورمات للهاتف وضبطه من جديد ولم يعمل الى ان تم تغيير الimei وجااهز .غريبه من قد وصله الجهاز هذا من قبل وشغله طبيعي؟\n"
            "جربوها بجوالات ثانيات يمكن تقرع !!!!\n\n"
            "#M_HORSE_PHONES\n"
            "#S25_Ultra\n"
            "#Programmer_RasheedModaghmer\n"
            "#VOLTE #LTE #CLONE"
        )
        bot.edit_message_text(display_text, user_id, call.message.message_id, reply_markup=markup)
        return

    # 7️⃣ معالج ثغرة تفعيل الفولتي لهواتف MTK
    elif cd == "rash_mtk_volte":
        track_tool("تفعيل الفولتي لهواتف MTK رشيد مدغمر", user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🎬 الانتقال لمشاهدة الشرح على فيسبوك", url="https://www.facebook.com/share/r/1DdtHk6S4C/?mibextid=wwXIfr"),
            types.InlineKeyboardButton("🔙 رجوع لقسم رشيد مدغمر", callback_data="sol_rasheed")
        )
        display_text = (
            "🔧 تفعيل الـ VoLTE لشبكات وعملاء هواتف معالجات MediaTek:\n\n"
            "🔥 الجزء الأخير والحاسم من سلسلة إعدادات Engineer Mode الحصرية والخاصة بأجهزة هواتف الـ MTK لشريحتي عالم الكارير والشبكات الصعبة.\n\n"
            "📱 **الشبكات المدعومة داخل الثغرة:**\n"
            "• أجهزة شبكة Cricket العالمية بثبات كامل.\n"
            "• أجهزة شبكة AT&T الحديثة بدون تعليق.\n\n"
            "#المبرمج_رشيد_مدغمر \n"
            "#Rasheed #volte #MTK #EngineerMode #Cricket #ATT #MediaTek #Android"
        )
        bot.edit_message_text(display_text, user_id, call.message.message_id, reply_markup=markup)
        return

    # 8️⃣ معالج ثغرة تفعيل VoLTE لهواتف LG
    elif cd == "rash_lg_volte":
        track_tool("تفعيل VoLTE لهواتف LG رشيد مدغمر", user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🎬 الانتقال لمشاهدة الشرح على فيسبوك", url="https://www.facebook.com/share/r/1947EtzJUY/?mibextid=wwXIfr"),
            types.InlineKeyboardButton("🔙 رجوع لقسم رشيد مدغمر", callback_data="sol_rasheed")
        )
        display_text = (
            "📱 الطريقة الصحيحة لتفعيل VoLTE لهواتف LG (شرح سريع)\n\n"
            "في هذا الفيديو أوضح لكم طريقة تفعيل خدمة ال #volte على هواتف LG بخطوات بسيطة وسريعة\n\n"
            "🎬 هذا المقطع هو شرح مختصر (ريلز)\n"
            "📺 الشرح الكامل متوفر على قناتي في اليوتيوب: Programmer-RasheedModaghmer\n\n"
            "لا تنسوا دعم الفيديو بالإعجاب 👍 ومشاركته ليستفيد الجميع 💡\n\n"
            "#LG #VoLTE #تفعيل_VoLTE #هواتف_LG #شروحات_اندرويد #Android #تقنية #شرح_تقني #4G #تحسين_المكالمات #ريلز #Reels #يوتيوب"
        )
        bot.edit_message_text(display_text, user_id, call.message.message_id, reply_markup=markup)
        return

    # 9️⃣ معالج فتح أكواد Engineer Mode لهواتف TCL وغيرها
    elif cd == "rash_open_eng_mode":
        track_tool("فتح اكواد Engineer Mode رشيد مدغمر", user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🎬 الانتقال لمشاهدة الشرح على فيسبوك", url="https://www.facebook.com/share/r/1DsYfYH1wN/?mibextid=wwXIfr"),
            types.InlineKeyboardButton("🔙 رجوع لقسم رشيد مدغمر", callback_data="sol_rasheed")
        )
        display_text = (
            "🔧 إذا لم تعمل أكواد Engineer Mode في هاتفك.. إليك الطريقة المضمونة لفتحها!\n\n"
            "If Engineer Mode codes aren't working on your phone 🔧, here's the guaranteed way to unlock them!\n\n"
            "#TCL #Engineer_mode #Rasheed_Modaghmer #EngineerMode #هندسة_الهاتف #اكواد_الهواتف #اسرار_الهواتف #صيانة_الموبايل"
        )
        bot.edit_message_text(display_text, user_id, call.message.message_id, reply_markup=markup)
        return

    # 🔟 معالج تجاوز شاشة Activation بدون كمبيوتر
    elif cd == "rash_bypass_activation":
        track_tool("تجاوز شاشة Activation بدون كمبيوتر", user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🎬 الانتقال لمشاهدة الشرح على فيسبوك", url="https://www.facebook.com/share/r/1CYAKe7Y4j/?mibextid=wwXIfr"),
            types.InlineKeyboardButton("🔙 رجوع لقسم رشيد مدغمر", callback_data="sol_rasheed")
        )
        display_text = (
            "طريقة تجاوز شاشة Activation (تنشيط الجهاز) بدون كمبيوتر \n"
            "How to bypass the activation screen (device activation) without a computer\n\n"
            "في هذا الفيديو، أشارككم الطريقة الصحيحة والمجربة لتجاوز قفل التنشيط بدون لابتوب.\n\n"
            "#رشيد_مدغمر #تجاوز_شاشة_التنشيط #Activation_Lock #برمجة_هواتف #صيانة_موبايلات #تكنولوجيا #حلول_تقنية #Unlock #PhoneRepair #Yemen_Mobile"
        )
        bot.edit_message_text(display_text, user_id, call.message.message_id, reply_markup=markup)
        return

    # 1️⃣1️⃣ معالج فتح خيارات المطور للايفون الكوبي
    elif cd == "rash_clone_developer":
        track_tool("خيارات المطور للايفون الكوبي", user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🎬 الانتقال لمشاهدة الشرح على فيسبوك", url="https://www.facebook.com/share/r/1Do91w5fqM/?mibextid=wwXIfr"),
            types.InlineKeyboardButton("🔙 رجوع لقسم رشيد مدغمر", callback_data="sol_rasheed")
        )
        display_text = (
            "📲 أسرار الآيفون الصيني: كيف تفتح خيارات المطور المخفي في الايفون الكوبي ؟\n"
            "Secrets of the Chinese iPhone: How to unlock the hidden developer options on a copycat iPhone?\n\n"
            "#آيفون_مقلد #خيارات_المطور #برمجة_هواتف #صنعاء #اليمن #iPhoneClone #DeveloperOptions #AndroidTips #رشيد_مدغمر"
        )
        bot.edit_message_text(display_text, user_id, call.message.message_id, reply_markup=markup)
        return

    # 1️⃣2️⃣ معالج استخراج رموز قفل التطبيقات عبر setedit
    elif cd == "rash_setedit_apps_lock":
        track_tool("استخراج قفل التطبيقات عبر setedit", user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🎬 الانتقال لمشاهدة الشرح على فيسبوك", url="https://www.facebook.com/share/r/14fXAMKGktm/?mibextid=wwXIfr"),
            types.InlineKeyboardButton("🔙 رجوع لقسم رشيد مدغمر", callback_data="sol_rasheed")
        )
        display_text = (
            "في هذا الفيديو أشرح طريقة استخراج رموز قفل التطبيقات المخزّنة داخل النظام باستخدام تطبيق setedit — بدون فورمات وبدون فقدان بياناتك.\n\n"
            "📱 الطريقة مفيدة خصوصًا لمن:\n"
            "✅ نسي رمز قفل التطبيقات\n"
            "✅ يريد استرجاع الوصول لتطبيقاته\n"
            "✅ يهتم بمعرفة كيف يُخزّن النظام هذه البيانات\n\n"
            "⚠️ ملاحظة: الفيديو تعليمي فقط لشرح نقطة ضعف موجودة في بعض الأجهزة (الطريقة تعمل فقط في بعض الأجهزة).\n\n"
            "▶️ شاهد الفيديو، وإذا استفدت لا تنسَ الإعجاب والمشاركة ليستفيد غيرك \n"
            "#أندرويد #تقنية #حماية #استرجاع_الرمز #Android #Tech"
        )
        bot.edit_message_text(display_text, user_id, call.message.message_id, reply_markup=markup)
        return

    # 1️⃣3️⃣ معالج تفعيل الـ VoLTE لهواتف Revvl يدوي
    elif cd == "rash_revvl_volte":
        track_tool("تفعيل VoLTE لهواتف Revvl", user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🎬 الانتقال لمشاهدة الشرح على فيسبوك", url="https://www.facebook.com/share/r/1DYhjz7pUL/?mibextid=wwXIfr"),
            types.InlineKeyboardButton("🔙 رجوع لقسم رشيد مدغمر", callback_data="sol_rasheed")
        )
        display_text = (
            "📶 فتح قائمة ال #volte وتفعيل ال #فولتي لهواتف #revvl يدوي بنجاح وبأسهل الخطوات.\n\n"
            "#revvl #volte #فولتي #secret_codes"
        )
        bot.edit_message_text(display_text, user_id, call.message.message_id, reply_markup=markup)
        return

    # 1️⃣4️⃣ معالج حل مشكلة عدم عمل VoLTE في أجهزة سامسونج
    elif cd == "rash_samsung_volte_fix":
        track_tool("حل مشكلة VoLTE سامسونج رشيد", user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🎬 الانتقال لمشاهدة الشرح على فيسبوك", url="https://www.facebook.com/share/r/1TtX56DoXG/?mibextid=wwXIfr"),
            types.InlineKeyboardButton("🔙 رجوع لقسم رشيد مدغمر", callback_data="sol_rasheed")
        )
        display_text = (
            "📶 في هواتف سامسونج ضبطت كل الإعدادات والVoLTE ما زال لا يعمل؟ شاهد هذا الفيديو الحاسم!\n\n"
            "On your Samsung phone, you've adjusted all the settings, but VoLTE still isn't working? Watch this video\n\n"
            "#ثواني_معاي… #فرق_كبير_معك #volte #samung #secret"
        )
        bot.edit_message_text(display_text, user_id, call.message.message_id, reply_markup=markup)
        return

    # 1️⃣5️⃣ معالج أسرار وفكفكة هواتف Vortex وتعديل الـ IMEI
    elif cd == "rash_vortex_fix":
        track_tool("أسرار وفكفكة هواتف Vortex", user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🎬 الانتقال لمشاهدة الشرح على فيسبوك", url="https://www.facebook.com/share/r/17oUxMZJFV/?mibextid=wwXIfr"),
            types.InlineKeyboardButton("🔙 رجوع لقسم رشيد مدغمر", callback_data="sol_rasheed")
        )
        display_text = (
            "🌀 السر صار بين أيديكم.. جربوا وانطلقوا فوراً!\n\n"
            "صلحوا الخربان وجربوا تفكفكوا الصالح.. فكفكه من حق المبرمجين مش من حق الصيانة 😉🔥\n\n"
            "#vortex #imei #android #Engneer_mode #secret #volte"
        )
        bot.edit_message_text(display_text, user_id, call.message.message_id, reply_markup=markup)
        return

    # 1️⃣6️⃣ معالج فتح قائمة إصلاح الرقم التسلسلي لهواتف Coolpad
    elif cd == "rash_coolpad_imei":
        if 'track_tool' in globals(): track_tool("اصلاح السيريال Coolpad رشيد", user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🎬 مشاهدة الشرح المباشر على يوتيوب", url="https://youtube.com/shorts/NJ5qhnjGUOc?si=Gx1_Yu_ArKDV3_f5"),
            types.InlineKeyboardButton("🔙 رجوع لقسم رشيد مدغمر", callback_data="sol_rasheed")
        )
        display_text = (
            "🛠️ **فتح قائمة إصلاح الرقم التسلسلي (IMEI) لهواتف Coolpad:**\n\n"
            "شرح وكود حصري للوصول إلى القائمة المخفية الخاصة بإصلاح وكتابة الرقم التسلسلي (السيريال) في هواتف كول باد (Coolpad) بكل سهولة لتفعيل الشبكة بنجاح.\n\n"
            "🎬 **اضغط على زر السيرفر أدناه لمشاهدة الخطوات وتطبيق الكود عبر الفيديو (Shorts):**"
        )
        bot.edit_message_text(display_text, user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        return

    # ===== معالج عرض شاشة الآيفون على الكمبيوتر (قسم الهدايا) =====
    elif cd == "gift_iphone_screen_mirror":
        try: bot.answer_callback_query(call.id)
        except: pass
        if 'track_tool' in globals(): track_tool("عرض شاشة الآيفون على الكمبيوتر", user_id)
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🎬 مشاهدة الشرح على يوتيوب", url="https://youtu.be/Y3spa6koDnI?si=0vcyNy3UW2fC6FBl"),
            types.InlineKeyboardButton("📥 تحميل أداة Reflector 4 (الموقع الرسمي)", url="https://www.airsquirrels.com/reflector/download"),
            types.InlineKeyboardButton("🔙 رجوع لقسم الهدايا", callback_data="gift_section") 
        )
        
        display_text = (
            "📱 **عرض شاشة الآيفون على شاشة الكمبيوتر مجاناً + تفعيل:**\n\n"
            "في هذا الفيديو ستشاهد:\n"
            "• طريقة ربط الآيفون بالكمبيوتر عبر ميزة انعكاس الشاشة (Screen Mirroring).\n"
            "• عرض سلس وبدقة عالية باستخدام أداة **Reflector 4**.\n"
            "• إعداد سريع وتحكم مباشر وبسيط.\n\n"
            "🔑 **كود التفعيل مدى الحياة:**\n"
            "تم توفير التفعيل لعيونكم.. اضغط على الكود بالأسفل لنسخه تلقائياً:\n\n"
            "`K3MMY7-SVT5RG-3PXFQ7-LAMMDH-K9QKEZ-EL689L`\n\n"
            "━━━━━━━━━━━━━━━━━\n"
            "👇 **استخدم الأزرار أدناه للتحميل ومشاهدة الشرح:**"
        )
        
        bot.edit_message_text(
            display_text, user_id, call.message.message_id, 
            reply_markup=markup, parse_mode="Markdown"
        )
        return
        
        bot.edit_message_text(
            display_text, user_id, call.message.message_id, 
            reply_markup=markup, parse_mode="Markdown"
        )
        return

    # 1️⃣7️⃣ معالج فتح قائمة تفعيل الباندات لهواتف mtk coolpad
    elif cd == "rash_coolpad_bands":
        if 'track_tool' in globals(): track_tool("تفعيل باندات Coolpad MTK رشيد", user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🎬 مشاهدة الشرح المباشر على يوتيوب", url="https://youtube.com/shorts/a8Toa_7plek?si=QrRCnmWeg5fUATEr"),
            types.InlineKeyboardButton("🔙 رجوع لقسم رشيد مدغمر", callback_data="sol_rasheed")
        )
        display_text = (
            "📶 **فتح قائمة تفعيل الباندات لهواتف MTK Coolpad:**\n\n"
            "شرح حصري لكيفية الدخول إلى إعدادات الشبكة وتفعيل الباندات (Bands) المخفية في هواتف كول باد التي تعمل بمعالجات MediaTek (MTK) لتحسين وتثبيت التغطية.\n\n"
            "🎬 **اضغط على زر السيرفر أدناه لمشاهدة الخطوات وتطبيق الكود عبر الفيديو (Shorts):**"
        )
        bot.edit_message_text(display_text, user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        return

# 🔓 معالج لوحة قسم فتح شفرات مجاناً (محدث ومقسم لشركات مصنعة - مضاف له Oneplus)
    elif cd == "sol_free_unlock":
        track_tool("قسم فتح الشفرات المجاني", user_id)
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("📱 Samsung", callback_data="unl_sub_samsung"),
            types.InlineKeyboardButton("📱 LG", callback_data="unl_sub_lg"),
        )
        markup.add(
            types.InlineKeyboardButton("📱 Redmi", callback_data="unl_sub_redmi"),
            types.InlineKeyboardButton("📱 Moto", callback_data="unl_sub_moto"),
        )
        # إبقاء زر الشرائح الإلكترونية مستقلاً بوسط القائمة ليكون عريضاً
        markup.add(
            types.InlineKeyboardButton("📟 فتح شفرة شرائح إلكترونية 🆓", callback_data="unl_sub_esim")
        )
        markup.add(
            types.InlineKeyboardButton("📱 Oneplus", callback_data="unl_sub_oneplus"), # 🌟 الخيار الجديد المضاف هنا
            types.InlineKeyboardButton("🌐 عام", callback_data="unl_sub_general"),
        )
        markup.add(types.InlineKeyboardButton("🔙 رجوع لقسم الحلول الرئيسي", callback_data="phone_solutions_main"))
        bot.edit_message_text(
            "🆓 **قسم فتح الشفرات مجاناً:**\n\n"
            "تم تنظيم وتصنيف الحلول لتسهيل الوصول إلى الشروحات والملفات المجانية.\n\n"
            "💡 **اختر قسم الشركة المصنعة أو الخدمة أدناه لتصفح الحلول المتاحة:**",
            user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown"
        )
        return

# 🧩 معالج الأقسام الفرعية الذكي للباقي (تم سحب الشرائح الإلكترونية منه لتزويده بالملفات)
    elif cd in ["unl_sub_samsung", "unl_sub_lg", "unl_sub_redmi", "unl_sub_moto", "unl_sub_oneplus"]:
        brands = {
            "unl_sub_samsung": "Samsung", 
            "unl_sub_lg": "LG", 
            "unl_sub_redmi": "Redmi",
            "unl_sub_moto": "Moto",
            "unl_sub_oneplus": "Oneplus"
        }
        brand_name = brands.get(cd, "الهواتف")
        track_tool(f"قسم شفرات {brand_name}", user_id)
        
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙 رجوع للأقسام", callback_data="sol_free_unlock"))
        bot.edit_message_text(
            f"📱 **قسم فتح شفرات {brand_name} مجاناً:**\n\n"
            f"⏳ **قريباً...**\n\nهذا القسم قيد التجهيز والرفع حالياً، وسيتم تزويده بأحدث طرق وملفات فك شفرات {brand_name} مجاناً فوراً! 😍🔥",
            user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown"
        )
        return

   # ===== 📱 قسم أنظمة نادرة: REDMI 12C =====
    elif cd == "rare_redmi_12c":
        try: bot.answer_callback_query(call.id)
        except: pass
        
        display_text = (
            "📱 **حل مشكلة تدمير النظام لهاتف REDMI 12C**\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "📌 **منقول عن الأخ/ ماجد المسوري:**\n\n"
            "إذا واجهتك مشكلة في هاتف **REDMI 12C**:\n"
            "• ظهور رسالة: *(تم تدمير النظام / System has been destroyed)*.\n"
            "• الجهاز على تحديث HyperOS.\n"
            "• محاولة فتح البوتلودر عبر أي أداة لا تنجح لعدم توفر الدعم.\n\n"
            "💡 **الحل:**\n"
            "قم بتحميل الفلاشة المناسبة من الرابط أدناه وتفليشها، وسيعمل الجهاز بشكل طبيعي وبدون مشاكل.\n"
            "━━━━━━━━━━━━━━━━━━"
        )
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🖼️ مشاهدة صور المشكلة والحل", url="https://t.me/haithamMax1/1088"),
            types.InlineKeyboardButton("📥 تحميل الفلاشة المناسبة", url="https://mifirm.net/download/9275?fbclid=IwdGRleAUYE7ZwZG9mBWZkaWQWUOlTHvOrcZqS2pQVVigxuRVzgUDbMmV4dG4DYWVtAjExAHNydGMGYXBwX2lkCjY2Mjg1NjgzNzkAAR5IcHdOWz84CEwwBsONMfxjaOgabaDcxgMjW7GlFiwOIEgIDhnoTZQOLdDInw_aem_bGXeXQYzE6Z6xHQdN_TwIQ"),
            types.InlineKeyboardButton("🔙 العودة لقائمة هواتف شاومي", callback_data="rare_brand_مجانية_Redmi")
        )
        
        try:
            bot.edit_message_text(
                display_text, 
                call.message.chat.id, call.message.message_id, 
                reply_markup=markup, parse_mode="Markdown"
            )
        except Exception as e:
            print(f"❌ خطأ في قسم Redmi 12C: {e}")
        return

    # 📟 معالج لوحة قسم الشرائح الإلكترونية (eSIM) وتزويده بالشروحات الجديدة
    elif cd == "unl_sub_esim":
        track_tool("قسم شفرات الشرائح الإلكترونية (eSIM)", user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("📟 ون بلاس BE2028 وضبط الشريحة", callback_data="esim_oneplus_be2028"),
            types.InlineKeyboardButton("📶 إصلاح تغطية يمن موبايل VoLTE (ون بلس وموتورولا)", callback_data="esim_volte_moto_op"),
            types.InlineKeyboardButton("🔙 رجوع للأقسام الرئيسية", callback_data="sol_free_unlock")
        )
        bot.edit_message_text(
            "📟 **قسم فتح شفرات وضبط الشرائح الإلكترونية (eSIM) مجاناً:**\n\n"
            "مرحباً بك في القسم المخصص لحلول ومشاكل الشرائح الإلكترونية لأحدث الأجهزة العالمية.\n\n"
            "💡 **اختر الخدمة البرمجية المطلوبة أدناه لعرض الشرح ورابط الفيديو المباشر:**",
            user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown"
        )
        return

    # 1️⃣ صفحة أزرار خدمة ون بلاس BE2028 شريحة إلكترونية
    elif cd == "esim_oneplus_be2028":
        track_tool("شرح ون بلاس BE2028 شريحة إلكترونية", user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🎬 اضغط هنا لمشاهدة شرح الفيديو", url="https://youtu.be/OxESWiRBNB8"),
            types.InlineKeyboardButton("🔙 رجوع لقسم الشرائح", callback_data="unl_sub_esim")
        )
        display_text = (
            "🔓 **فك شفرة ون بلاس BE2028 وضبط الشريحه الإلكتروني**\n\n"
            "🔥 الشرح الكامل والمجرب لتفعيل وضبط التغطية وفك قفل الشبكة لجهاز OnePlus BE2028 بنجاح.\n\n"
            "🎬 اضغط على زر السيرفر أدناه لمتابعة خطوات الشرح بالفيديو مباشرة:"
        )
        bot.edit_message_text(display_text, user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        return

    # 2️⃣ صفحة أزرار خدمة إصلاح تغطية يمن موبايل فولتي ون بلس وموتورولا
    elif cd == "esim_volte_moto_op":
        track_tool("شرح VoLTE شريحة إلكترونية ون بلس وموتورولا", user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🎬 اضغط هنا لمشاهدة شرح الفيديو", url="https://youtu.be/TXK984o_WPc"),
            types.InlineKeyboardButton("🔙 رجوع لقسم الشرائح", callback_data="unl_sub_esim")
        )
        display_text = (
            "📶 **اصلاح تغطية يمن موبايل فولتي شريحة اكتروني أجهزة ون بلس و موتورولا**\n"
            "`oneplus n30 VoLTE motorola`\n\n"
            "🔥 حل مشكلة تفعيل نظام الـ VoLTE للشرائح الإلكترونية على أجهزة OnePlus N30 وموديلات Motorola الحديثة لتشغيل التغطية بنجاح.\n\n"
            "🎬 اضغط على زر السيرفر أدناه لمتابعة خطوات الشرح بالفيديو مباشرة:"
        )
        bot.edit_message_text(display_text, user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        return
# معالج قسم الشرح النصي المطور بعد إضافة زر S21 Ultra الجديد
    # معالج قسم الشرح النصي المطور
    elif cd == "sol_text":
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("📱 حل مشاكل A326U , S326DL , A136U , A216U , S127DL", callback_data="sol_text_mtk_fix"),
            types.InlineKeyboardButton("📶 حل مشكلة شريحة يمن موبايل لهاتف S21 Ultra 5G", callback_data="sol_text_s21_yemen"),
        )
        markup.add(
            types.InlineKeyboardButton("🔓 تخطي حماية Bypass KNOX", callback_data="page_text_bypass_knox")
        )
        # 🌟 الزر المنقول من قسم اليوتيوب
        markup.add(
            types.InlineKeyboardButton("📺 حل مشكلة البرامج غير مدعومة (Redmi Note 12 5G)", callback_data="sol_yt_redmi_fix")
        )
        markup.add(
            types.InlineKeyboardButton("🔙 رجوع لقسم الحلول الرئيسي", callback_data="phone_solutions_main")
        )
        
        bot.edit_message_text(
            "📝 <b>قسم الشروحات النصية المضمونة لمشاكل الهواتف:</b>\n\nاختر الشرح المتاح والمجرب أدناه للتطبيق والاستفادة:",
            user_id, call.message.message_id, reply_markup=markup, parse_mode="HTML"
        )
        return

    # 🔓 معالج خيار تخطي Bypass KNOX لمعالجات Exynos
    elif cd == "page_text_bypass_knox":
        track_tool("شرح تخطي Bypass KNOX", user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            # ✅ تم تعديل الكولباك ليرجع لقائمة sol_text بشكل صحيح
            types.InlineKeyboardButton("🔙 رجوع لقسم الشروحات", callback_data="sol_text")
        )
        
        knox_desc = (
            "🔓 **تخطي KNOX / MDM / KG لهواتف سامسونج**\n"
            "📱 *المخصصة للأجهزة التي تعمل بمعالجات Exynos*\n\n"
            "⚙️ **الخطوات والتعليمات بالتفصيل:**\n\n"
            "1️⃣ قم بتفعيل نظام **ADB Root** أولاً عن طريق أداة `MOBILedit`.\n\n"
            "2️⃣ افتح واجهة السطر البرمجي `cmd` على الكمبيوتر واكتب الأمر التالي لفتح تطبيق الاتصال بداخل الهاتف تلقائياً:\n"
            "`adb shell am start -n com.samsung.android.dialer/.DialerActivity`\n\n"
            "3️⃣ اكتب الرمز التالي في لوحة اتصال الهاتف: `*#0808#` ثم اختر منها خيار `RNDIS+ACM+DM` لكي يتعرف الكمبيوتر على الكوم بورت (Port) الخاص بالجهاز.\n\n"
            "4️⃣ افتح أداة `QCDMA` أو أي أداة احترافية أخرى تدعم ميزة التخطي.\n\n"
            "5️⃣ من خانة **FRP** بداخل الأداة، اختر الأمر **Bypass KNOX** واعتمد طريقة الرمز المعروفة `*#0*#`.\n\n"
            "🎉 **ومبروك عليك تخطي الحماية وتجاوزها بنجاح تام!**\n\n"
            "━━━━━━━━━━━━━━━━━\n"
            "📊 **الأجهزة التي تمت تجربة الطريقة عليها بنجاح:**\n"
            "• Samsung A13 (`SM-A135U`)\n"
            "• Samsung XCover Pro (`SM-G715U`)"
        )
        
        bot.edit_message_text(
            knox_desc, user_id, call.message.message_id,
            reply_markup=markup, parse_mode="Markdown"
        )

    # ✅ معالج شرح مشكلة هواتف معالجات MTK (تم إصلاحه كلياً بنظام HTML لمنع تجميد البوت)
    elif cd == "sol_text_mtk_fix":
        track_tool("شرح حل مشاكل معالجات MTK", user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🔙 رجوع لقسم الشرح النصي", callback_data="sol_text")
        )
        
        display_text = (
            '<a href="https://t.me/haithamMax1/887">&#8203;</a>' # 📸 كود سحب الصورة المخفي والمستقر كلياً في نظام HTML
            "📱 <b>حل مشاكل هواتف معالجات MTK العالقة:</b>\n\n"
            "أحياناً عند التعامل مع هواتف معالجات MTK مثل:\n"
            "<code>A326U , S326DL , A136U , A216U , S127DL</code>\n\n"
            "📌 <b>قد تواجهك إحدى هذه المشكلات:</b>\n"
            "1/ الهاتف لا يقبل الدخول لوضع الـ Brom\n"
            "2/ الهاتف يظل معلق على وضعية الـ Brom ولا يقبل الخروج منها\n"
            "3/ يظل الهاتف معلق وحانب بوضعية Download mode\n\n"
            "⚙️ <b>طريقة الحل الشاملة:</b>\n"
            "فيما يلي شرح لكيفية التعامل مع هذه المشكلات عن طريق الأداة الرائعة والمميزة:\n"
            "🔥 <b>Fastunlocker pro</b>\n\n"
            "⚠️ <i>وبحجر الله يا فريق سام للبرمجيات اذكروا المصدر مش نسخ ولصق ودعممه 😅😂</i>\n\n"
            "━━━━━━━━━━━━━━━━━\n"
            "🤝 <b>مع تحيات فريق برمجة موبايل (للمبرمجين فقط)</b>\n"
            "🔗 <a href='https://t.me/BrmagaMobile'>https://t.me/BrmagaMobile</a>"
        )
        bot.edit_message_text(display_text, user_id, call.message.message_id, reply_markup=markup, parse_mode="HTML")
        return

    # 📶 لوحة اختيار طرق حل مشكلة S21 Ultra يمن موبايل
    elif cd == "sol_text_s21_yemen":
        track_tool("قائمة حل مشكلة S21 يمن موبايل", user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("📋 الطريقة الأولى: (الطريقة المنقولة)", callback_data="s21_method_1"),
            types.InlineKeyboardButton("👑 الطريقة الثانية: (خاصة بـ هيثم ماكس)", callback_data="s21_method_2"),
            types.InlineKeyboardButton("🔙 رجوع لقسم الشرح النصي", callback_data="sol_text")
        )
        bot.edit_message_text(
            "📶 **مشكلة شريحة يمن موبايل لهاتف S21 Ultra 5G بعد الفورمات:**\n\n"
            "المشكلة: بعد الفورمات لم يشتغل شريحة يمن موبايل لا اتصال ولا بيانات.\n\n"
            "💡 **اختر الطريقة البرمجية التي تود عرضها لتطبيق الحل الحاسم:**",
            user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown"
        )
        return

    # 📋 عرض تفاصيل الطريقة الأولى (المنقولة)
    elif cd == "s21_method_1":
        track_tool("S21 يمن موبايل - الطريقة المنقولة", user_id)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙 رجوع لخيارات الطرق", callback_data="sol_text_s21_yemen"))
        
        display_text = (
            "📋 **الطريقة الأولى (المنقولة) - حل مشكلة S21 Ultra 5G:**\n\n"
            "📌 **خطوات تشغيل الاتصال والبيانات بعد الفورمات:**\n"
            "1️⃣ تحويل الهاتف لنظام فرايزون عبر أي أداة داعمة لتغيير الـ CSC.\n"
            "2️⃣ ركب شريحة يمن موبايل وقم بإعادة تشغيل الهاتف.\n"
            "3️⃣ حذف بوليسي مان (Policy Manager) ثم ركب شريحة فرايزون واعد التشغيل مرة أخرى.\n"
            "4️⃣ إيقاف رسالة تحويل الكارير من أي أداة داعمة بواسطة الشريحة.\n"
            "5️⃣ ركب شريحة يمن موبايل وسيشتغل معك الاتصال فوراً على طول.\n\n"
            "🌐 **بالنسبة لبيانات الفورجي (4G):**\n"
            "الضبط والتفعيل يكون حسب الموديل لأي أداة داعمة.\n\n"
            "💡 *إضافة:* إذا ما نفع الشرح معك، قم بتركيب شريحة فولتي (VoLTE).\n"
            "━━━━━━━━━━━━━━━━━\n"
            "✨ Done..."
        )
        bot.edit_message_text(display_text, user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        return

    # 👑 عرض تفاصيل الطريقة الثانية (طريقة هيثم ماكس الخاصة والسرية)
    elif cd == "s21_method_2":
        track_tool("S21 يمن موبايل - طريقة هيثم ماكس", user_id)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙 رجوع لخيارات الطرق", callback_data="sol_text_s21_yemen"))
        
        display_text = (
            "👑 **الطريقة الثانية (حصرياً وخاصة بـ هيثم ماكس) - حل مشكلة S21 Ultra 5G:**\n\n"
            "⚡ **الخطوات الاحترافية والسرية الفعالة:**\n"
            "1️⃣ إخراج الشريحة من الهاتف تماماً.\n"
            "2️⃣ تحويل الكارير CSC من أداة `SamFw` إلى **Sprint**.\n"
            "3️⃣ تحويل الكارير CSC من أداة `SamFw` إلى **BST**.\n"
            "4️⃣ إدخال الشريحة؛ إذا اشتغلت افتح برنامج الشبكة (Network Mode) وقم بتغيير الوضع والتردد إلى **CDMA** أو **LTE**.\n"
            "5️⃣ إرجاع الكارير إلى فرايزون أو اسبرنت للتثبيت المستقر والنهائي للشبكة.\n"
            "━━━━━━━━━━━━━━━━━\n"
            "🦅 تم الحل بنجاح كالمعتاد مع تحيات ابراهيم الصيري!"
        )
        bot.edit_message_text(display_text, user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        return

   # معالج قسم شروحات اليوتيوب المطور   # معالج قسم شروحات اليوتيوب المطور (محدث بالـ 3 أزرار الجديدة لـ TCL)
    # معالج قسم شروحات اليوتيوب المطور (بعد نقل شرح شاومي)
    # معالج قسم شروحات اليوتيوب المطور
    elif cd == "sol_youtube":
        try: bot.answer_callback_query(call.id)
        except: pass
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("📺 FRP TCL 40 XE T609L", callback_data="sol_yt_tcl_t609l"),
            types.InlineKeyboardButton("📺 FRP Motorola Moto G Fast XT2045-3", callback_data="sol_yt_moto_xt2045"),
            types.InlineKeyboardButton("📺 FRP Motorola Moto G Pure XT2163", callback_data="sol_yt_moto_xt2163"),
            types.InlineKeyboardButton("📺 New Bypass FRP TCL K24 T434D", callback_data="sol_yt_tcl_k24"),
            types.InlineKeyboardButton("📺 New Bypass FRP TCL K11 T432W", callback_data="sol_yt_tcl_k11"),
            types.InlineKeyboardButton("📺 New Bypass FRP TCL A507DL A2", callback_data="sol_yt_tcl_a507"),
            types.InlineKeyboardButton("🚫 إيقاف الرد التلقائي للمكالمات (هواتف شاومي)", callback_data="youtube_xiaomi_auto_answer"),
            types.InlineKeyboardButton("📺 Reset Frp FOXXD A65U", callback_data="sol_yt_foxxd_a65u"), # 🌟 الزر الجديد المضاف هنا
            types.InlineKeyboardButton("🔙 رجوع لقسم الحلول الرئيسي", callback_data="phone_solutions_main")
        )
        bot.edit_message_text(
            "📺 **قسم الشروحات المرئية المضمونة لمشاكل الهواتف:**\n\nاختر الشرح المرئي المتاح أدناه للمشاهدة والتطبيق والاستفادة:",
            call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown"
        )
        return

    # معالج شرح فيديو تخطي حساب جوجل وحل مشكلة البرامج لشياومي (الحصري)
    elif cd == "sol_yt_redmi_fix":
        track_tool("شرح يوتيوب حل مشكلة البرامج غير مدعومة", user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🎬 اضغط هنا لمشاهدة الشرح على يوتيوب", url="https://m.youtube.com/watch?v=woydpMu6rc0"),
            types.InlineKeyboardButton("🔙 رجوع لقسم الشرح النصي", callback_data="sol_text") # 🌟 تم تغيير مسار الرجوع
        )
        display_text = (
            "📺 **تخطي حساب جوجل لجوال Redmi note 12 5G:**\n\n"
            "🔥 **مع حل مشكلة البرامج غير مدعومة سواءً كان البوتلودر مفتوح أو مغلق 🌚 وبدون تفليش روم بالكامل!**\n\n"
            "📌 **تفاصيل الشرح البرمجي:**\n"
            "شرح مرئي متكامل يحل لك مشكلة تعليق أو رفض البرامج للعمل بعد عمليات التخطي على الحمايات الحديثة لأجهزة شاومي بدون خسارة الوقت في تفليش فلاشات كاملة.\n\n"
            "━━━━━━━━━━━━━━━━━\n"
            "🔄 *الطريقة منقولة من قناة المهندس: سعيد الزعزعي*\n"
            "💐 *والشكر الكبير والتقدير للباش مهندس: عبدالله العيدروس*\n"
            "━━━━━━━━━━━━━━━━━\n"
            "🎬 للمشاهدة المباشرة للخطوات على اليوتيوب، اضغط أدناه:"
        )
        bot.edit_message_text(display_text, user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        return

    # 1️⃣ معالج شرح فيديو تخطي جوجل جوال TCL K24
    elif cd == "sol_yt_tcl_k24":
        track_tool("شرح يوتيوب تخطي FRP TCL K24", user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🎬 اضغط هنا لمشاهدة الشرح على يوتيوب", url="https://youtu.be/aHN1YnslJx4"),
            types.InlineKeyboardButton("🔙 رجوع لقسم اليوتيوب", callback_data="sol_youtube")
        )
        display_text = (
            "📺 **New Bypass FRP TCL K24 T434D:**\n\n"
            "🔥 **شرح حصري واحترافي لتخطي حماية حساب جوجل (FRP) لأجهزة TCL الحديثة!**\n\n"
            "📌 **تفاصيل الشرح البرمجي:**\n"
            "طريقة قوية ومجربة لتجاوز قفل جوجل بنجاح وثبات تاف وبدون أي تعقيد بوضعية حماية 2026.\n"
            "━━━━━━━━━━━━━━━━━\n"
            "🦅 تم الحل بنجاح كالمعتاد مع تحيات ابراهيم الصيري!\n\n"
            "🎬 للمشاهدة المباشرة للخطوات على اليوتيوب، اضغط أدناه:"
        )
        bot.edit_message_text(display_text, user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        return

    # 2️⃣ معالج شرح فيديو تخطي جوجل جوال TCL K11
    elif cd == "sol_yt_tcl_k11":
        track_tool("شرح يوتيوب تخطي FRP TCL K11", user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🎬 اضغط هنا لمشاهدة الشرح على يوتيوب", url="https://youtu.be/85XhrheNTDo"),
            types.InlineKeyboardButton("🔙 رجوع لقسم اليوتيوب", callback_data="sol_youtube")
        )
        display_text = (
            "📺 **New Bypass FRP TCL K11 T432W:**\n\n"
            "🔥 **تجاوز قفل حساب جوجل (FRP) لجوال TCL K11 بكل سهولة وانسيابية!**\n\n"
            "📌 **تفاصيل الشرح البرمجي:**\n"
            "ثغرة ممتازة وجديدة كلياً مخصصة لفك ثغرة الحماية بأمان تام وبأقل خطوات برمجية ممكنة.\n"
            "━━━━━━━━━━━━━━━━━\n"
            "🦅 تم الحل والتقفيل بنجاح كالمعتاد مع تحيات هيثم ماكس!\n\n"
            "🎬 للمشاهدة المباشرة للخطوات على اليوتيوب، اضغط أدناه:"
        )
        bot.edit_message_text(display_text, user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        return

    # 3️⃣ معالج شرح فيديو تخطي جوجل جوال TCL A507DL A2
    elif cd == "sol_yt_tcl_a507":
        track_tool("شرح يوتيوب تخطي FRP TCL A507DL", user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🎬 اضغط هنا لمشاهدة الشرح على يوتيوب", url="https://youtu.be/s4X0X45eZ28"),
            types.InlineKeyboardButton("🔙 رجوع لقسم اليوتيوب", callback_data="sol_youtube")
        )
        display_text = (
            "📺 **New Bypass FRP TCL A507DL A2:**\n\n"
            "🔥 **التخطي النهائي لحساب جوجل (FRP) لهاتف TCL A507DL الحماية الصعبة!**\n\n"
            "📌 **تفاصيل الشرح البرمجي:**\n"
            "حل حاسم ومجرب ومضمون 100% لواحدة من أعقد حمايات هاتف TCL A2 بوضوح وسلاسة عالية.\n"
            "━━━━━━━━━━━━━━━━━\n"
            "🦅 تم الحل بنجاح كالمعتاد مع تحيات ابراهيم الصيري!\n\n"
            "🎬 للمشاهدة المباشرة للخطوات على اليوتيوب، اضغط أدناه:"
        )
        bot.edit_message_text(display_text, user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        return

    # 🌟 معالج شرح فيديو تخطي FOXXD A65U
    elif cd == "sol_yt_foxxd_a65u":
        try: bot.answer_callback_query(call.id)
        except: pass
        if 'track_tool' in globals(): track_tool("شرح فيديو تخطي FOXXD A65U", user_id)
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🎬 اضغط هنا لمشاهدة الشرح مباشرة", url="https://www.facebook.com/share/v/1P1jsZnu2z/?mibextid=wwXIfr"),
            types.InlineKeyboardButton("🔙 رجوع لقسم الشروحات المرئية", callback_data="sol_youtube")
        )
        
        display_text = (
            "📺 **Reset Frp FOXXD A65U | Bypass google account Free:**\n\n"
            "🔥 **مجاناً للجميع شرح كيف تخطي حساب هاتف فوكسد موديل A65U!**\n\n"
            "📌 **تفاصيل الشرح:**\n"
            "طريقة فعالة ومجانية بالكامل لتجاوز قفل حساب جوجل (FRP) لهذا الموديل بنجاح وبدون تعقيد.\n\n"
            "👤 **بواسطة المبرمج:** عبد الرقيب محمد حاجب\n"
            "━━━━━━━━━━━━━━━━━\n"
            "🎬 للمشاهدة المباشرة للخطوات عبر الفيديو، اضغط أدناه:"
        )
        
        bot.edit_message_text(display_text, user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        return

    elif cd == "sol_yt_moto_xt2163":
        try: bot.answer_callback_query(call.id)
        except: pass
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🎬 اضغط هنا لمشاهدة الشرح على يوتيوب", url="https://youtu.be/jMiHCwQBbdo"),
            types.InlineKeyboardButton("🔙 رجوع لقسم اليوتيوب", callback_data="sol_youtube")
        )
        bot.edit_message_text(
            "📺 **شرح FRP Motorola Moto G Pure XT2163:**\n\n"
            "تمت إضافة الشرح التقني المضمون لتخطي حماية حساب جوجل لهذا الجهاز.\n\n"
            "ملاحظة: تأكد من مطابقة إصدار الحماية قبل البدء.",
            call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown"
        )
        return

    elif cd == "sol_yt_tcl_t609l":
        try: bot.answer_callback_query(call.id)
        except: pass
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🎬 اضغط هنا لمشاهدة الشرح على يوتيوب", url="https://youtu.be/P3Cnn5mIK_w"),
            types.InlineKeyboardButton("🔙 رجوع لقسم اليوتيوب", callback_data="sol_youtube")
        )
        bot.edit_message_text(
            "📺 **تخطي حساب جوجل FRP - TCL 40 XE (T609L):**\n\n"
            "شرح مرئي دقيق لتخطي حماية حساب جوجل (FRP) لهذا الإصدار من شركة TCL.\n\n"
            "🎬 للمشاهدة المباشرة، اضغط على الزر أدناه:",
            call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown"
        )
        return

    elif cd == "sol_yt_moto_xt2045":
        try: bot.answer_callback_query(call.id)
        except: pass
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🎬 اضغط هنا لمشاهدة الشرح على يوتيوب", url="https://youtu.be/JWP-W1DkK-sP"),
            types.InlineKeyboardButton("🔙 رجوع لقسم اليوتيوب", callback_data="sol_youtube")
        )
        bot.edit_message_text(
            "📺 **تخطي حساب جوجل FRP - Motorola Moto G Fast (XT2045-3):**\n\n"
            "شرح مرئي احترافي ومباشر لتخطي الحماية الأمنية لهذا الطراز بكل سهولة.\n\n"
            "🎬 للمشاهدة المباشرة، اضغط على الزر أدناه:",
            call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown"
        )
        return

    # ===== معالج زر إيقاف الرد التلقائي للمكالمات (شاومي) =====
    elif cd == "youtube_xiaomi_auto_answer":
        try: bot.answer_callback_query(call.id)
        except: pass
        if 'track_tool' in globals(): track_tool("إيقاف الرد التلقائي شاومي", user_id)
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🎬 مشاهدة الشرح المباشر (Shorts)", url="https://youtube.com/shorts/McoeDcAd6DQ?si=JKqCZZU9Jf8KHqig"),
            types.InlineKeyboardButton("👤 فيسبوك - Omar Programmer", url="https://www.facebook.com/share/p/1CV3F5NoeG/"),
            
            # 🌟 تم تعديل زر الرجوع هنا.. تأكد أن الكلمة "youtube" تطابق اسم قسم اليوتيوب في ملفك
            types.InlineKeyboardButton("🔙 رجوع لقسم يوتيوب", callback_data="youtube") 
        )
        
        display_text = (
            "🚫 **خطوات إيقاف ميزة \"الرد التلقائي\" للمكالمات في هواتف شاومي:**\n\n"
            "يعاني البعض من مشكلة رد الهاتف التلقائي على المكالمات دون تدخل منهم في أجهزة Xiaomi.\n"
            "إليك الخطوات السريعة لحل هذه المشكلة:\n\n"
            "1️⃣ ادخل إلى **الإعدادات (Settings)**.\n"
            "2️⃣ اذهب إلى **التطبيقات (Apps)**.\n"
            "3️⃣ اختر **إعدادات تطبيقات النظام**.\n"
            "4️⃣ ادخل على **إعدادات الاتصال**.\n"
            "5️⃣ اختر **الرد التلقائي (Auto-answer)** وقم بتعطيله (إيقاف).\n\n"
            "🌟 **المنشور منقول من المبدع:** [Omar Programmer]\n\n"
            "👇 **لمشاهدة الشرح بالفيديو وتطبيق الخطوات عملياً، اضغط على الأزرار أدناه:**"
        )
        
        bot.edit_message_text(
            display_text, user_id, call.message.message_id, 
            reply_markup=markup, parse_mode="Markdown"
        )
        return

    


    # معالج قسم الملفات المتبقي المعين له "قريباً"
    elif cd == "sol_files":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙 رجوع لقسم الحلول", callback_data="phone_solutions_main"))
        
        bot.edit_message_text(
            "⏳ **قريباً...**\n\nهذا القسم قيد التجهيز والرفع حالياً، وسيتم تزويده بأحدث الملفات الحصرية والمضمونة قريباً جداً! 😍🔥",
            user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown"
        )
        return

    # ================= 🆕 معالج برنامج تصوير الشاشة الحصري في قسم الهدايا =================
    elif cd == "gift_screen_recorder":
        track_tool("برنامج تصوير الشاشة للابتوب", user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("📥 اضغط هنا للتحميل المباشر من ميديا فاير", url="https://www.mediafire.com/file/f6cv7heduztxjcv/3uRecorder.zip/file"),
            types.InlineKeyboardButton("🔙 رجوع لقسم الهدايا", callback_data="gift_section")
        )
        
        display_text = (
            "🎬 **برنامج 3uRecorder (أفضل برنامج لتصوير شاشة اللابتوب):**\n\n"
            "🔒 **حقوق النشر محفوظة، ولن تجدوا هذا البرنامج الحصري والنادر إلا عند هيثم ماكس!**\n\n"
            "📌 **أبرز ميزات ووظائف البرنامج:**\n"
            "• **خفيف جداً:** لا يستهلك من موارد المعالج ولا يسبب أي ثقل أو بطء أثناء الألعاب أو الشروحات والبرمجة.\n"
            "• **دقة عالية:** يدعم تسجيل الشاشة بجودة HD Full نقية تماماً وبدون أي تفتيت بالصورة.\n"
            "• **نقاوة صوت احترافية:** التقاط الصوت الداخلي للكمبيوتر والخارجي من المايك بصفاء تام وبدون أي تشويش.\n"
            "• **حجم مثالي مضغوط:** حجم ملف الفيديو الناتج خفيف جداً لتوفير مساحة الهارد ديسك للابتوب.\n"
            "━━━━━━━━━━━━━━━━━\n"
            "📥 للتحميل المباشر والسريع عبر سيرفر الميديا فاير، اضغط أدناه:"
        )
        bot.edit_message_text(display_text, user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        return

    # ==========================================
    # 🏴‍☠️ قسم الأدوات المكركة الموثوقة
    # ==========================================
    elif cd == "trusted_cracked_tools":
        try: bot.answer_callback_query(call.id)
        except: pass
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("Unlock Tool crack ", callback_data="unlocktool_crack_2026"),
            # 🌟 تم إضافة زر Muslim Odin الجديد هنا
            types.InlineKeyboardButton("Muslim Odin v5.0 crack_2026", callback_data="muslim_odin_crack_2026"),
            types.InlineKeyboardButton("🔙 رجوع", callback_data="menu_tools_section")
        )
        
        text = (
            "🏴‍☠️ **قسم الأدوات المكركة الموثوقة:**\n\n"
            "مرحباً بك في القسم المخصص للأدوات المكركة المجربة والموثوقة.\n"
            "👇 **اختر الأداة التي ترغب في تصفحها:**"
        )
        bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        return

    # ==========================================
    # 🔓 تفاصيل Unlock Tool Crack 2026
    # ==========================================
    elif cd == "unlocktool_crack_2026":
        try: bot.answer_callback_query(call.id)
        except: pass
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🔗 رابط ", url="https://mega.nz/file/AgBBWQSL#2OfoI7tUdOeLbMXTq6bzlpRyuYqAdo6nc6jITy2P4sQ"),
            types.InlineKeyboardButton("🔗 رابط الأداة", url="https://file.unlocktool.net/"),
            types.InlineKeyboardButton("📺 شرح كيفية التثبيت", url="https://www.facebook.com/share/v/1LZmE3Fn6H/"),
            types.InlineKeyboardButton("🔙 رجوع", callback_data="trusted_cracked_tools")
        )
        
        text = (
            "🔓 **Unlock Tool crack **\n\n"
            "نشكر الأخ / **RE Guru** على نشر الكراك وتوفيره للجميع 🌹\n"
            "💬 **رابط مجموعته:** [اضغط هنا للدخول](https://t.me/RE_Guru)\n\n"
            "⚠️ **تنبيه وإخلاء مسؤولية:**\n"
            "كل شخص يستخدمه يتحمل المسؤولية الكاملة، ويُفضل استخدامه على لابتوب آخر (جهاز ثانوي).. الكراك مجرب وشغال طبيعي 💯\n\n"
            "👇 **اختر الإجراء الذي تريده من الأزرار أدناه:**"
        )
        
        bot.edit_message_text(
            text, user_id, call.message.message_id, 
            reply_markup=markup, disable_web_page_preview=True, parse_mode="Markdown"
        )
        return

    # ==========================================
    # 🔓 تفاصيل Muslim Odin v5.0 Crack 2026
    # ==========================================
    elif cd == "muslim_odin_crack_2026":
        try: bot.answer_callback_query(call.id)
        except: pass
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🔗 Muslim Odin v5.0", url="https://www.mediafire.com/file/cykov66b65e72gd/Muslim_Odin_v5.0_By_Ali_Hassani_%252B212676866794.exe.rar/file"),
            types.InlineKeyboardButton("🔗 Mtk Pro v54", url="https://www.mediafire.com/file/c58gccgipz1xn4f/M.t.k_Pro_v54_installer_By_ALi_Hassani.zip/file"),
            types.InlineKeyboardButton("🔗 Muslim Apple Tool v20", url="https://www.mediafire.com/file/wxygb966uy25hoh/installer._.Muslim_Apple_Tool_V20_By_ALi_Hassani.zip/file"),
            types.InlineKeyboardButton("🔗 Muslim Odin A12+ v4.0", url="https://www.mediafire.com/file/styuz1h2lgk70dv/installer__Muslim_Odin_A12%252B_v4.0_By_ALi_Hassani.zip/file"),
            types.InlineKeyboardButton("🔑 Muslim Odin License Activation Tool", url="https://www.mediafire.com/file/d7urtu8l79xo4tu/RE_GURU.zip/file"),
            types.InlineKeyboardButton("🔙 رجوع", callback_data="trusted_cracked_tools")
        )
        
        text = (
            "🔓 **كراك Muslim Odin v5.0 crack_2026**\n\n"
            "نشكر الأخ / **RE Guru** على نشر الكراك وتوفيره للجميع 🌹\n"
            "💬 **رابط مجموعته:** [اضغط هنا للدخول](https://t.me/RE_Guru)\n\n"
            "🔑 **كلمة سر فك الضغط:** `123456`\n\n"
            "⚠️ **تنبيه وإخلاء مسؤولية:**\n"
            "كل شخص يستخدمه يتحمل المسؤولية الكاملة، ويُفضل استخدامه على لابتوب آخر (جهاز ثانوي).. الكراك مجرب وشغال طبيعي 💯\n\n"
            "👇 **اختر الأداة التي تريد تحميلها من الأزرار أدناه:**"
        )
        
        bot.edit_message_text(
            text, user_id, call.message.message_id, 
            reply_markup=markup, disable_web_page_preview=True, parse_mode="Markdown"
        )
        return

    # ================= 🚀 قسم كأس العالم للايفون بالوصف الجديد والروابط الرسمية =================
    elif cd == "iphone_worldcup_app":
        track_tool("برنامج قنوات كأس العالم للايفون", user_id)
        
        try:
            bot.delete_message(user_id, call.message.message_id)
        except:
            pass

        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("⬇️ اضغط هنا لتنزيل البرنامج من App Store", url="https://apps.apple.com/us/app/vozi-pro/id6779024508?l=ar"),
            types.InlineKeyboardButton("🔙 رجوع لقسم الهدايا", callback_data="gift_section")
        )
        
        # 📝 الوصف الجديد والمعدل بالكامل بناءً على طلبك
        display_text = (
            "📺 **تطبيق جديد للايفون 🍏😍:**\n\n"
            "يمكنك مشاهدة من خلاله مباريات كأس العالم بالكامل مع تصميم بسيط.\n"
            "حمّل تطبيق **Vozi Pro** واستمتع بمتابعة جميع المباريات، والقنوات بجودة عالية 😍🔥\n\n"
            "‼️ **هام جدًا** ‼️\n"
            "بعد تحميل التطبيق، يُرجى إدخال رمز التفعيل: `22455` داخل التطبيق، ثم النقر على زر **Open Playlist** ليعمل التطبيق بشكل صحيح.\n\n"
            "نتمنى من الجميع مشاركة التطبيق على مواقع التواصل الاجتماعي، لتكبر عائلة Buz أكثر 😍❤️\n\n"
            "⚠️ *هام* : التطبيق معرض للحذف قبل ساعات قليلة لهذا يرجى تحميله بسرعة!"
        )
        
        # الروابط الرسمية المأخوذة من قناتك مباشرة لضمان العمل 100%
        photo1 = "https://t.me/haithamMax1/876"
        photo2 = "https://t.me/haithamMax1/877"

        media = [
            types.InputMediaPhoto(photo1, caption=display_text, parse_mode="Markdown"),
            types.InputMediaPhoto(photo2)
        ]
        
        try:
            bot.send_media_group(user_id, media)
            bot.send_message(user_id, "⚙️ **روابط ومفاتيح التحكم:**", reply_markup=markup, parse_mode="Markdown")
        except Exception as e:
            print(f"Error sending media group: {e}")
            bot.send_message(user_id, display_text, reply_markup=markup, parse_mode="Markdown")
        return
 
    # ================= 🆕 معالج تفعيل Adobe Creative Cloud المجاني =================
    elif cd == "adobe_cloud_gift":
        track_tool("تفعيل Adobe Creative Cloud", user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🔗 اضغط هنا للدخول والتفعيل المباشر", url="https://commerce.adobe.com/store/checkout?items%5B0%5D%5Bid%5D=D0440AB0F2F7F2F2CB39657F45BC5D56&items%5B0%5D%5Bq%5D=1&cli=ace&co=IN&ref-order-id=D646F17C1FD5517747959836178529&utm_medium=Email&utm_campaign=GMI%20%3A%20CLCM%20Abandon_Cart_Reminder_WWEN&correlationId=f54aa9ff-26f3-4464-8c2b-559fb9568d94-0&utm_source=chatgpt.com"),
            types.InlineKeyboardButton("🔙 رجوع لقسم الهدايا", callback_data="gift_section")
        )
        
        display_text = (
            "💻 **تفعيل Adobe Creative Cloud 4M مجاناً:**\n\n"
            "📌 **التعليمات والخطوات بالتفصيل:**\n\n"
            "💘. انقر فوق زر الرابط أدناه لبدء التفعيل.\n"
            "💘. سوف ترى صفحة الدفع الرسمية التي تظهر فيها القيمة بقيمة **0$**.\n"
            "💘. أضف بطاقتك (الفيزا/الماستر) وقم بقبول الاشتراك المتجدد تلقائيًا.\n"
            "💘. لن يتم فرض أو سحب أي رسوم مالية أثناء التفعيل نهائياً.\n\n"
            "✅ **بعد إتمام التفعيل بنجاح:**\n"
            "- افتح تطبيقك المصرفي أو إعدادات الدفع داخل حساب أدوبي.\n"
            "- قم بإلغاء الاشتراك / التجديد التلقائي على الفور لحماية بطاقتك.\n\n"
            "💬 إذا واجهت أي مشاكل أثناء التفعيل، فلا تتردد في مراسلتي خاص.\n\n"
            "👍 **نصائح موصى بها للعمل:**\n"
            "- استخدم متصفحاً جديداً تماماً أو وضع التصفح الخفي.\n"
            "- إذا لم يتم قبول البطاقة، فحاول تشغيل تطبيق Surfshark VPN لتخطي الحماية.\n"
            "━━━━━━━━━━━━━━━━━\n"
            "🛒 للبدء الفوري بالتفعيل والحصول على الـ 4 أشهر، اضغط أدناه:"
        )
        bot.edit_message_text(display_text, user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        return

    # ===== قنوات الأخبار =====
    elif cd == "news_channels":
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("🟢 توثيقات (1)", url=WHATSAPP_CHANNEL_1),
            types.InlineKeyboardButton("🟢 واتساب (2)",  url=WHATSAPP_CHANNEL_2),
        )
        markup.add(
            types.InlineKeyboardButton("🔵 قناة التيلجرام", url=CHANNEL_URL),
            types.InlineKeyboardButton("🔙 رجوع",            callback_data="back_start"),
        )
        bot.edit_message_text(
            "📢 **قنوات الأخبار والتوثيقات:**",
            user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown"
        )

    # ===== التواصل =====
    elif cd == "main_contact":
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("📱 واتساب",  url=WHATSAPP_URL),
            types.InlineKeyboardButton("👤 تيلجرام", url=TELEGRAM_ADMIN),
        )
        markup.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="back_start"))
        bot.edit_message_text(
            "💬 **تواصل معي خاص:**\nاختر وسيلة التواصل:",
            user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown"
        )

    # ===== تحديث الادوات_التعاريف =====
    elif cd == "main_android":
        # 1. إيقاف الدائرة الدوارة فوراً لمنع تعليق الزر في شاشة المشترك
        bot.answer_callback_query(call.id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
        # 🌟 السر هنا: تغيير row_width إلى 1 لفرش الأزرار بالكامل بشكل عريض سطر بسطر
            types.InlineKeyboardButton("💎 تحديثات الادوات",   callback_data="main_tools"),
            types.InlineKeyboardButton("📡 قسم التعاريف",       callback_data="main_drivers"),
            types.InlineKeyboardButton("📥 مواقع الأنظمة",      callback_data="main_firmware_sites"),
            types.InlineKeyboardButton("🔓 فك الشفرات",         callback_data="main_unlocking"),
            types.InlineKeyboardButton("🔙 رجوع",               callback_data="back_start"),
        )   
                       
        bot.edit_message_text(
            "📦 **تحديث الادوات والتعاريف:**\n\nاختر القسم الذي تريده من القائمة أدناه:", 
            user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown"
        )
        return


    elif cd == "main_tools":
        try: bot.answer_callback_query(call.id)
        except: pass
        markup = types.InlineKeyboardMarkup(row_width=2)
        btns = [types.InlineKeyboardButton(v[0], callback_data=f"link_tools_{k}") for k, v in DATA["tools"].items()]
        markup.add(*btns)
        # 🌟 تم التعديل هنا ليعود للرئيسية مباشرة
        markup.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="back_start"))
        bot.edit_message_text("💎 **تحديثات الادوات الحصرية:**", user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        return

    
    # معالج أزرار تحديثات الادوات لمنع تجمدها وتحويل الروابط لأزرار تحميل
    elif cd.startswith("link_tools_"):
        try: bot.answer_callback_query(call.id)
        except: pass
        
        key = cd.replace("link_tools_", "")
        if "tools" in DATA and key in DATA["tools"]:
            tool_name, link = DATA["tools"][key]
            if 'track_tool' in globals(): track_tool(tool_name, user_id)
            
            # 💡 عرض الأوصاف المخصصة والاحترافية
            if key == "android_utility":
                display_text = (
                    "🛠️ **أداة AndroidUtility.v200 (النسخة العملاقة الحصرية):**\n\n"
                    "تعتبر من أقوى الأدوات المجانية الشاملة لكل فنيي صيانة السوفت وير، وتدعم عمليات معقدة بضغطة زر واحدة لترسانة ضخمة من الهواتف.\n\n"
                    "📌 **أبرز ميزات ووظائف الأداة:**\n"
                    "• **معالجات MediaTek (MTK):** تخطي حماية المعالج (BROM Auth Bypass)، فورمات آمن، قراءة البيانات، وإصلاح السيريال.\n"
                    "• **معالجات Qualcomm:** إدخال الأجهزة لوضع الـ EDL وتفليش وتخطي حمايات الحسابات.\n"
                    "• **أجهزة Samsung:** تفعيل وضع الـ ADB عبر الثغرات الحديثة، تخطي حساب جوجل (FRP)، وإصلاح حلقة الإقلاع.\n"
                    "• **أجهزة Xiaomi & Huawei:** تخطي حسابات مي (Mi Account) وحسابات هواوي، وعمل سحب للفلاشات الرسمية.\n"
                    "• **ميزات إضافية:** تخطي حمايات أجهزة الأوبو والـ ريلمي والـ فيفو بنقرة زر وبأمان تام.\n\n"
                    "⚠️ **ملاحظة هامة قبل التشغيل:**\n"
                    "يرجى إيقاف تشغيل مانع الفيروسات (Windows Defender) قبل فك الضغط عن الملف حتى لا يحذف ملفات التشغيل الأساسية للأداة.\n"
                    "━━━━━━━━━━━━━━━━━\n"
                    "📥 للتحميل المباشر والسريع عبر سيرفر الميديا فاير، اضغط أدناه:"
                )

            
            elif key == "tsm_edition":
                try: bot.answer_callback_query(call.id)
                except: pass
                display_text = hmaxi18n.translate_static_content(
                    "tsm_edition",
                    TSM_EDITION_DESCRIPTION,
                    hmaxi18n.get_language(user_id),
                )

            else:
                # عرض النص الافتراضي المنسق لبقية الأدوات الشائعة
                display_text = f"💎 **تحميل {tool_name}:**\n\nاضغط على الزر أدناه لبدء تحميل النسخة الرسمية والمحدثة للأداة مباشرة:"
            
            markup = types.InlineKeyboardMarkup(row_width=1)
            if link.startswith("http"):
                markup.add(types.InlineKeyboardButton("⬇️ اضغط للتحميل المباشر", url=link))
            markup.add(types.InlineKeyboardButton("🔙 رجوع للأدوات", callback_data="main_tools"))
            
            bot.edit_message_text(display_text, user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        else:
            bot.answer_callback_query(call.id, "❌ لم يتم العثور على الأداة المطلوبة.", show_alert=True)
        return
    
  
    elif cd == "main_drivers":
        try: bot.answer_callback_query(call.id)
        except: pass
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        
        # 🌟 السر هنا: قمنا بتحويل الأزرار لروابط مباشرة (URL) لتصبح مثل زر ADB تماماً!
        # (استخدمنا شرطاً ذكياً: إذا كان يحتوي على رابط يجعله مباشراً، وإلا يتركه كقائمة)
        btns = [
            types.InlineKeyboardButton(v[0], url=v[1]) if str(v[1]).startswith("http")
            else types.InlineKeyboardButton(v[0], callback_data=f"link_drivers_{k}")
            for k, v in DATA["drivers"].items()
        ]
        markup.add(*btns)
        
        # زر تعاريف هواوي (يفتح قائمة فرعية)
        markup.add(types.InlineKeyboardButton("⚙️ Huawei usb driver", callback_data="huawei_drivers_menu"))
        
        # زر ADB Installer (مباشر)
        markup.add(types.InlineKeyboardButton("⬇️ ADB Installer v1.4.2", url="https://www.mediafire.com/file/22ko126iuh42w21/15+Second+ADB+Installer+v1.4.2.zip/file"))
        
        # زر الرجوع للرئيسية
        markup.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="back_start"))
        
        bot.edit_message_text(
            "📡 **قسم التعريفات الشامل والذكي:**\n\n"
            "💡 *جميع الأزرار أصبحت روابط مباشرة، اضغط على أي تعريف للتحميل فوراً:*", 
            user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown"
        )
        return



    # 2️⃣ القسم الثاني: نافذة روابط هواوي الـ 4 (سيتم لصقها تلقائياً تحت القسم الأول)
    elif cd == "huawei_drivers_menu":
        try: bot.answer_callback_query(call.id)
        except: pass
        
        if 'track_tool' in globals():
            track_tool("قسم تعاريف Huawei", user_id)
            
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("⬇️ Download Huawei ADB Driver", url="https://www.mediafire.com/file/o0x4xs2e6b4u846/latest_usb_driver_windows.zip/file"),
            types.InlineKeyboardButton("⬇️ Download Huawei Qualcomm Driver", url="https://www.mediafire.com/file/mclznqmya1s5i8c/qualcomm_driver.zip"),
            types.InlineKeyboardButton("⬇️ Download Huawei CDC Driver", url="https://www.mediafire.com/file/wr9d19ctlmyqfcr/android_cdc_driver.zip"),
            types.InlineKeyboardButton("⬇️ Download Huawei VCOM Driver", url="https://www.mediafire.com/file/facdq2tkdiajrs9/android_vcom_driver.zip"),
            types.InlineKeyboardButton("🔙 رجوع لقسم التعاريف", callback_data="main_drivers")
        )
        
        display_text = (
            "⚙️ **قسم تعاريف Huawei الشاملة:**\n\n"
            "مرحباً بك في القسم المخصص لتعريفات أجهزة هواوي لجميع المعالجات.\n"
            "💡 **اختر نوع التعريف الذي تبحث عنه للتحميل المباشر أدناه:**"
        )
        bot.edit_message_text(display_text, user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        return


    # معالج ضغطات أزرار التعاريف الخاص لمنع تجمدها وعرض الروابط الـ 4 الرسمية لـ SPD
    elif cd.startswith("link_drivers_"):
        key = cd.replace("link_drivers_", "")
        if "drivers" in DATA and key in DATA["drivers"]:
            tool_name, link = DATA["drivers"][key]
            track_tool(tool_name, user_id)
            
            # 💡 إذا اختار المستخدم تعاريف SPD، يتم عرض الـ 4 روابط الرسمية التي أرسلتها
            if key == "spd":
                display_text = (
                    "📲 **قسم تعاريف أجهزة SPD (Spreadtrum / Unisoc):**\n\n"
                    "تعتبر هذه التعاريف أساسية لربط هواتف SPD بالكمبيوتر بشكل مستقر بدون انقطاع أثناء عمليات السوفت وير وفك الحظر.\n\n"
                    "📥 **يرجى اختيار رابط تحميل الإصدار المناسب لجهازك:**"
                )
                
                markup = types.InlineKeyboardMarkup(row_width=1)
                markup.add(
                    types.InlineKeyboardButton("⬇️ SPRD UNISOC v4.21.39 (Official CM2)", url="https://www.mediafire.com/file_premium/jy0yomuk3mg0ncf/SPRD_UNISOC_4.21.39.134_pass-1111_official_by_cm2.7z/file"),
                    types.InlineKeyboardButton("⬇️ SPRD NPI USB Driver v1.4", url="https://www.mediafire.com/file_premium/ma7h9hc885no62b/SPRD_NPI_USBDriver_1.4.rar/file"),
                    types.InlineKeyboardButton("⬇️ SPD Driver R4.20 (إصدار 2020 المحدث)", url="https://www.mediafire.com/file_premium/k666rpz3wrgrfik/SPD_Driver_R4.20.4201%252814.Oct.2020_v4.20.42.134%2529.rar/file"),
                    types.InlineKeyboardButton("⬇️ SPD Drivers v2.0.0 (الإصدار الكلاسيكي)", url="https://www.mediafire.com/file/7gyts88vppidzuh/SPD.Drivers(04.April,2015_V2.0.0.131).rar/file"),
                    types.InlineKeyboardButton("🔙 رجوع لقائمة التعاريف", callback_data="main_drivers")
                )
            else:
                # 📡 العرض الافتراضي لبقية التعاريف العادية
                display_text = f"📡 **تحميل {tool_name}:**\n\nاضغط على الزر أدناه لبدء تحميل التعريف المطلوب مباشرة وبأقصى سرعة:"
                markup = types.InlineKeyboardMarkup(row_width=1)
                if link.startswith("http"):
                    markup.add(types.InlineKeyboardButton("⬇️ اضغط للتحميل المباشر", url=link))
                markup.add(types.InlineKeyboardButton("🔙 رجوع للتعاريف", callback_data="main_drivers"))
            
            bot.edit_message_text(display_text, user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        else:
            bot.answer_callback_query(call.id, "❌ لم يتم العثور على التعريف.")
        return
        
    elif cd == "main_unlocking":
        try: bot.answer_callback_query(call.id)
        except: pass
        markup = types.InlineKeyboardMarkup(row_width=2)
        btns = [types.InlineKeyboardButton(v[0], callback_data=f"link_unlocking_{k}") for k, v in DATA["unlocking"].items()]
        markup.add(*btns)
        # 🌟 تم التعديل هنا ليعود للرئيسية مباشرة
        markup.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="back_start"))
        bot.edit_message_text("🔓 **أدوات فك الشفرات المعتمدة:**", user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        return

    # معالج أزرار فك الشفرات لمنع تجمدها
    elif cd.startswith("link_unlocking_"):
        key = cd.replace("link_unlocking_", "")
        if "unlocking" in DATA and key in DATA["unlocking"]:
            tool_name, link = DATA["unlocking"][key]
            track_tool(tool_name, user_id)
            display_text = f"🔓 **أداة {tool_name}:**\n\nاضغط على الزر أدناه لبدء تحميل أداة فك الشفرات مباشرة:"
            markup = types.InlineKeyboardMarkup(row_width=1)
            if link.startswith("http"):
                markup.add(types.InlineKeyboardButton("⬇️ اضغط للتحميل المباشر", url=link))
            markup.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="main_unlocking"))
            bot.edit_message_text(display_text, user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        else:
            bot.answer_callback_query(call.id, "❌ لم يتم العثور على الأداة.")
        return

    elif cd == "main_firmware_sites":
        try: bot.answer_callback_query(call.id)
        except: pass
        markup = types.InlineKeyboardMarkup(row_width=2)
        btns = [types.InlineKeyboardButton(v[0], callback_data=f"link_firmware_sites_{k}") for k, v in DATA["firmware_sites"].items()]
        markup.add(*btns)
        # 🌟 تم التعديل هنا ليعود للرئيسية مباشرة
        markup.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="back_start"))
        bot.edit_message_text("📥 **مواقع تحميل الأنظمة الرسمية:**", user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        return

    # معالج أزرار مواقع الأنظمة والفلاشات لمنع تجمدها
    elif cd.startswith("link_firmware_sites_"):
        key = cd.replace("link_firmware_sites_", "")
        if "firmware_sites" in DATA and key in DATA["firmware_sites"]:
            tool_name, link = DATA["firmware_sites"][key]
            track_tool(tool_name, user_id)
            display_text = f"📥 **{tool_name}:**\n\nاضغط على الزر أدناه للانتقال للموقع الرسمي وتحميل الفلاشات:"
            markup = types.InlineKeyboardMarkup(row_width=1)
            if link.startswith("http"):
                markup.add(types.InlineKeyboardButton("🌐 الانتقال لموقع التحميل", url=link))
            markup.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="main_firmware_sites"))
            bot.edit_message_text(display_text, user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        else:
            bot.answer_callback_query(call.id, "❌ لم يتم العثور على الموقع.")
        return
        
        
        
        # ===== قسم الآيفون =====
        # ===== قسم الآيفون =====
        # ===== قسم الآيفون =====
    elif cd == "main_iphone":
        try: bot.answer_callback_query(call.id) # لفك التعليق
        except: pass
        
        # 🌟 تم تغيير العرض إلى 1 لتصبح الأزرار عريضة ومستقلة
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🛠️ IPHONE TOOLS",       callback_data="iphone_tools_list"),
            types.InlineKeyboardButton("💰 أسعار الآيكلود",     callback_data="icloud_prices"),
            types.InlineKeyboardButton("🔓 فتح شفرة الآيفون",  callback_data="iphone_unlock_menu"),
            types.InlineKeyboardButton("📱iOS 9.0x الى iOS 27.x", callback_data="iphone_bypass_menu"),
            types.InlineKeyboardButton("🔌 قطع الآيفون PWN", callback_data="iphone_pwn_parts"),
            types.InlineKeyboardButton("🔙 رجوع",               callback_data="back_start")
        )
        bot.edit_message_text("📱 **قسم IPHONE:**\nاختر أحد الخيارات أدناه:", user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        return

    # ===== 💰 أسعار الآيكلود =====
    elif cd == "icloud_prices":
        try: bot.answer_callback_query(call.id)
        except: pass
        if 'track_tool' in globals(): track_tool("أسعار الآيكلود", user_id)

        lang = hmaxi18n.get_language(user_id)
        icloud_texts = {
            "ar": ICLOUD_PRICES,
            "en": (
                "**💰 Updated official iCloud unlock price list:**\n\n"
                "📱 iPhone 11 series: **(100$)**\n"
                "📱 iPhone 12 series: **(115$)**\n"
                "📱 iPhone 13 series: **(125$)**\n"
                "📱 iPhone 14 series: **(135$)**\n"
                "📱 iPhone 15 series: **(150$)**\n"
                "📱 iPhone 16 series: **(175$)**\n"
                "📱 iPhone 17 series: **(250$)**\n\n"
                "⏳ **Service time:** 20-30 days\n"
                "━━━━━━━━━━━━━━━━━\n"
                "✅ To activate, contact the administration."
            ),
            "fr": (
                "**💰 Liste des prix officielle mise à jour pour le déblocage iCloud :**\n\n"
                "📱 iPhone 11 : **(100$)**\n"
                "📱 iPhone 12 : **(115$)**\n"
                "📱 iPhone 13 : **(125$)**\n"
                "📱 iPhone 14 : **(135$)**\n"
                "📱 iPhone 15 : **(150$)**\n"
                "📱 iPhone 16 : **(175$)**\n"
                "📱 iPhone 17 : **(250$)**\n\n"
                "⏳ **Délai du service :** 20-30 jours\n"
                "━━━━━━━━━━━━━━━━━\n"
                "✅ Pour activer, contactez l’administration."
            ),
        }
        back_labels = {"ar": "🔙 رجوع لقسم الآيفون", "en": "🔙 Back to iPhone", "fr": "🔙 Retour à iPhone"}
        contact_labels = {"ar": "💬 مراسلة الإدارة", "en": "💬 Contact admin", "fr": "💬 Contacter l’admin"}

        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton(
                contact_labels.get(lang, contact_labels["ar"]),
                url=f"tg://user?id={MY_CHAT_ID}",
            )
        )
        markup.add(
            types.InlineKeyboardButton(
                back_labels.get(lang, back_labels["ar"]),
                callback_data="main_iphone",
            )
        )
        bot.edit_message_text(
            icloud_texts.get(lang, icloud_texts["ar"]),
            user_id, call.message.message_id,
            reply_markup=markup, parse_mode="Markdown",
        )
        return

    # ===== 🍎 iTunes مدفوع =====
    elif cd == "page_iphone_itunes":
        try: bot.answer_callback_query(call.id)
        except: pass
        if 'track_tool' in globals(): track_tool("iTunes مدفوع", user_id)

        lang = hmaxi18n.get_language(user_id)
        itunes_texts = {
            "ar": ITUNES_PAID_DESC,
            "en": (
                "**🍎 Paid iTunes service**\n\n"
                "This service allows you to download apps and games from iTunes "
                "to your laptop and install them on any device.\n\n"
                "✅ To order the service, contact us using the buttons below:"
            ),
            "fr": (
                "**🍎 Service iTunes payant**\n\n"
                "Ce service vous permet de télécharger des applications et des jeux depuis iTunes "
                "sur votre ordinateur portable et de les installer sur n’importe quel appareil.\n\n"
                "✅ Pour commander le service, contactez-nous via les boutons ci-dessous :"
            ),
        }
        whatsapp_labels = {"ar": "📱 واتساب", "en": "📱 WhatsApp", "fr": "📱 WhatsApp"}
        telegram_labels = {"ar": "👤 تيلجرام", "en": "👤 Telegram", "fr": "👤 Telegram"}
        back_labels = {"ar": "🔙 رجوع", "en": "🔙 Back", "fr": "🔙 Retour"}

        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton(whatsapp_labels.get(lang, whatsapp_labels["ar"]), url=WHATSAPP_URL),
            types.InlineKeyboardButton(telegram_labels.get(lang, telegram_labels["ar"]), url=TELEGRAM_ADMIN),
        )
        markup.add(
            types.InlineKeyboardButton(
                back_labels.get(lang, back_labels["ar"]),
                callback_data="iphone_tools_list",
            )
        )
        bot.edit_message_text(
            itunes_texts.get(lang, itunes_texts["ar"]),
            user_id, call.message.message_id,
            reply_markup=markup, parse_mode="Markdown",
        )
        return

    elif cd == "iphone_tools_list":
        try: bot.answer_callback_query(call.id)
        except: pass
        
        # 🌟 تم تغيير العرض إلى 1 هنا أيضاً
        markup = types.InlineKeyboardMarkup(row_width=1)
        
        # 🛡️ جلب البيانات بأمان مع توفير نسخة احتياطية محلية
        iphone_data = DATA.get("iphone_tools", {
            "3utools_v3_28":  ("🛠️ 3utools V3.28", "https://www.mediafire.com/file/..."),
            "3utools_latest": ("🚀 3utools الأخير", "https://www.mediafire.com/file/..."),
            "itunes_paid":    ("🍎 itunes مدفوع", "page_iphone_itunes"),
        })
        
        btns = [
            types.InlineKeyboardButton(v[0], callback_data=v[1]) if v[1].startswith("page_")
            else types.InlineKeyboardButton(v[0], callback_data=f"link_iphone_tools_{k}")
            for k, v in iphone_data.items()
        ]
        markup.add(*btns)
        
        markup.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="main_iphone"))
        bot.edit_message_text(
            "🛠️ **أدوات IPHONE:**\n\nاختر الأداة المطلوبة من القائمة أدناه للبدء:", 
            user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown"
        )
        return


    # معالج ضغطات أزرار أدوات الآيفون الخاصة لمنع تجمدها
    # 🌟 معالج أزرار أدوات الآيفون المجانية (المطور لالتقاط أي زر بسرعة البرق)
    elif cd.startswith("link_free_iphone_") or cd.startswith("link_iphone_tools_"):
        try: bot.answer_callback_query(call.id)
        except: pass
        
        # التقاط المفتاح الصحيح للأداة
        key = cd.replace("link_free_iphone_", "").replace("link_iphone_tools_", "")
        
        # تحديد من أي قائمة سيأخذ البيانات
        tool_data = None
        if "free_iphone" in DATA and key in DATA["free_iphone"]:
            tool_data = DATA["free_iphone"][key]
        elif "iphone_tools" in DATA and key in DATA["iphone_tools"]:
            tool_data = DATA["iphone_tools"][key]
            
        if tool_data:
            tool_name, link = tool_data
            
            # تسجيل التفاعل للأداة
            if 'track_tool' in globals(): track_tool(tool_name, user_id)
            
            # ضبط وجهة الرجوع الذكية (إذا كانت مدفوعة يرجع لقائمة المدفوع، وإلا يرجع للمجاني)
            back_callback = "iphone_tools_list" if cd.startswith("link_iphone_tools_") else "main_free_tools"
            
            markup = types.InlineKeyboardMarkup(row_width=1)
            if link.startswith("http"):
                markup.add(types.InlineKeyboardButton("⬇️ اضغط للتحميل المباشر", url=link))
            markup.add(types.InlineKeyboardButton("🔙 رجوع للقائمة", callback_data=back_callback))
            
            display_text = f"🍏 **أداة {tool_name}:**\n\nاضغط على الزر أدناه لبدء تحميل أداة الآيفون المطلوبة مباشرة وبأقصى سرعة:"
            bot.edit_message_text(display_text, user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        else:
            bot.answer_callback_query(call.id, "❌ لم يتم العثور على أداة الآيفون.", show_alert=True)
        return

    # ===== فتح شفرة الآيفون =====
    elif cd == "iphone_unlock_menu":
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("📟 الأكواد شرائح إلكترونية", callback_data="iphone_unlock_esim_codes"),
            types.InlineKeyboardButton("📋 طريقة فتح الشفرة",        callback_data="iphone_unlock_method"),
            types.InlineKeyboardButton("📡 ملفات IPCC",              callback_data="iphone_unlock_ipcc"),
            types.InlineKeyboardButton("🔙 رجوع",                    callback_data="main_iphone"),
        )
        bot.edit_message_text(
            "🔓 **فتح شفرة الآيفون:**\nاختر الخدمة المطلوبة:",
            user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown"
        )

    elif cd == "iphone_unlock_esim_codes":
        track_tool("الأكواد شرائح إلكترونية", user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("📥 تحميل ملف الأكواد PDF", url=IPHONE_CODES_PDF_LINK),
            types.InlineKeyboardButton("🔙 رجوع",                   callback_data="iphone_unlock_menu"),
        )
        bot.edit_message_text(
            IPHONE_UNLOCK_CODES_DESC + "\n\n📥 يمكنك أيضاً تحميل ملف الأكواد PDF:",
            user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown"
        )

    elif cd == "iphone_unlock_method":
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("1️⃣ الطريقة الأولى",  callback_data="iphone_method_1"),
            types.InlineKeyboardButton("2️⃣ الطريقة الثانية", callback_data="iphone_method_2"),
            types.InlineKeyboardButton("🔙 رجوع",              callback_data="iphone_unlock_menu"),
        )
        bot.edit_message_text(
            "📋 **طريقة فتح الشفرة:**\nاختر الطريقة:",
            user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown"
        )

    elif cd == "iphone_method_1":
        track_tool("الطريقة الأولى - فتح شفرة", user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("📥 تحميل الطريقة الأولى", url=IPHONE_METHOD_1_LINK),
            types.InlineKeyboardButton("🔙 رجوع",                  callback_data="iphone_unlock_method"),
        )
        bot.edit_message_text(
            "1️⃣ **الطريقة الأولى لفتح الشفرة:**",
            user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown"
        )

    elif cd == "iphone_method_2":
        track_tool("الطريقة الثانية - فتح شفرة", user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("📥 تحميل الطريقة الثانية", url=IPHONE_METHOD_2_LINK),
            types.InlineKeyboardButton("🔙 رجوع",                   callback_data="iphone_unlock_method"),
        )
        bot.edit_message_text(
            "2️⃣ **الطريقة الثانية لفتح الشفرة:**",
            user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown"
        )

    # 📡 1. واجهة قسم ملفات ثبات التغطية IPCC بداخل أجهزة الآيفون
    elif cd == "iphone_unlock_ipcc":
        try:
            bot.answer_callback_query(call.id) # إنهاء علامة التحميل في الزر فوراً
            
            if 'track_tool' in globals():
                track_tool("ملفات ثبات التغطية IPCC", call.message.chat.id)
            
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(
                # تم توسيع القائمة لتشمل كل الأقسام الجديدة هندسياً وبصرياً
                types.InlineKeyboardButton("📱 26.5.1 أو 26.5 أو 26.5.2", callback_data="ipcc_multi_versions"),
                types.InlineKeyboardButton("📱 ملفات إصدار iOS 18.3.1", callback_data="ipcc_ios_18_3_1"),
                types.InlineKeyboardButton("🔥 ملفات إصدار iOS 18.4 & 18.4.1", callback_data="ipcc_ios_18_4_1"),
                types.InlineKeyboardButton("⚠️ تعليمات مهمه جداً", callback_data="ipcc_important_instructions"),
                types.InlineKeyboardButton("🔙 رجوع", callback_data="iphone_unlock_menu")
            )
            
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="📡 **ملفات ثبات التغطية IPCC**\n\nاختر الإصدار المطلوب من القائمة أدناه لعرض تفاصيل التنزيل والشرح:",
                reply_markup=markup,
                parse_mode="Markdown"
            )
        except Exception as e:
            print(f"❌ خطأ في قسم iphone_unlock_ipcc: {e}")
        return

    # 📥 2. معالج فتح خيار الإصدارات وعرض نص الشرح ورابط التحميل الأصلي
    elif cd == "ipcc_multi_versions":
        try:
            bot.answer_callback_query(call.id) # إنهاء علامة التحميل في الزر فوراً
            
            if 'track_tool' in globals():
                track_tool("عرض ملفات IPCC عادل بن شعيب", call.message.chat.id)
            
            mediafire_link = "https://www.mediafire.com/file/hacpi77edsvqfc4/Iphone+26.5.2.ipcc/file"
            
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(
                types.InlineKeyboardButton("📥 اضغط هنا لتنزيل الملف مباشرة", url=mediafire_link),
                types.InlineKeyboardButton("🔙 رجوع للقائمة", callback_data="iphone_unlock_ipcc")
            )
            
            # النص والشرح والوسوم بالملي مثلما أرسلتها بدون أي تعديل خارجي
            display_text = (
                "شكرا للاخ عادل بن شعيب \n\n"
                "#وصل الجديد 🔥\n\n"
                "#ملفات شبكة يمن موبايل لسلسلة ايفونات 13 ✅\n\n"
                "لآخر اصدار حق امس 🔥\n\n"
                "iOS 26.5.2 ⬅️\n\n"
                "ويدعم ايضاً كلاً من الاصدار\n\n"
                "26.5 \n\n"
                "و\n\n"
                "26.5.1\n\n"
                "بنفس طريقة الثبات المشروحة من قبل 👍\n\n\n"
                "⬅️ لتزيل الملف 👇\n"
                f"{mediafire_link}"
            )
            
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=display_text,
                reply_markup=markup,
                parse_mode="Markdown",
                disable_web_page_preview=True # يمنع ظهور معاينات الروابط الطويلة المزعجة بالرسالة
            )
        except Exception as e:
            print(f"❌ خطأ في قسم ipcc_multi_versions: {e}")
        return

    # ===== 🍏 القائمة الفرعية: تخطي الآيفون (لقسم IPHONE) =====
    elif cd == "iphone_bypass_menu":
        try: bot.answer_callback_query(call.id)
        except: pass
        
        text = (
            "🍏 **قسم تخطي الآيفون (iOS 9.0x إلى iOS 27.x)**\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "يرجى اختيار القسم المناسب لجهازك من الخيارات أدناه:"
        )
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("📱 A12 & A13 Bionic (XR to 11 Pro Max, SE2, iPads)", callback_data="iphone_a12_a13"),
            types.InlineKeyboardButton("🔓 iOS 9.0 حتى iOS 26.1 (بدون شبكة)", callback_data="iphone_legacy_bypass"),
            types.InlineKeyboardButton("🔙 العودة لقسم الآيفون", callback_data="main_iphone") # تأكد من اسم callback قسم الايفون الرئيسي لديك
        )
        
        try:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        except Exception as e:
            print(f"❌ خطأ: {e}")
        return

    # ===== 📱 الخيار الأول: A12 & A13 Bionic =====
    elif cd == "iphone_a12_a13":
        try: bot.answer_callback_query(call.id)
        except: pass
        
        text = (
            "📱 **A12 & A13 Bionic (XR to 11 Pro Max, SE2, iPads)**\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "📌 **أبرز محطات الإصدار:**\n"
            "• دعم كامل لشرائح Apple A12 و A13 Bionic على iOS 17.x، 18.x، 26.x، و27.x.\n"
            "• تجاوز Hello Bypass بنقرة واحدة مع الحفاظ على الرقم التسلسلي الأصلي (دون تغيير).\n"
            "• مساعد DFU مدمج مع مؤقتات عد تنازلي في الوقت الحقيقي واستغلال BootROM لتقنية USBliter8.\n"
            "• سلسلة إقلاع رامديسك آلية ذات 10 خطوات مع حقن ديناميكي SPTM وTXM.\n"
            "• محرك تركيب مزدوج APFS مع نظام احتياطي تلقائي (طريقة التركيب 2).\n"
            "• معدل رقم تسلسلي مدمج بوضع البنفسجي لتفعيل Hello بديل.\n"
            "• نافذة منبثقة لمعرف Apple ID ورقم الهاتف وقارئ حساب المالك الفوري.\n\n"
            "⚠️ **ملاحظة هامة:** لازم توصيلة خاصة بالآيفون لإدخال الهاتف في وضع PWN.\n"
            "━━━━━━━━━━━━━━━━━━"
        )
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("📥 رابط الأداة", url="https://mega.nz/file/Yi90RBZI#LU-6ncaPvFkce8bAuq5Yj5t8GsAOZRgFcH8mjfHCNLc"),
            types.InlineKeyboardButton("📝 اضغط هنا لتسجيل الجهاز ECID", url="https://iunlock.cloud/register?tool=ramdisk-pro"),
            types.InlineKeyboardButton("📺 فيديو تعليمي", url="https://youtu.be/I2o66eFSKpw?is=1_83NCf5UnGTftoS"),
            types.InlineKeyboardButton("🔙 العودة للقائمة السابقة", callback_data="iphone_bypass_menu")
        )
        
        try:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        except Exception as e:
            print(f"❌ خطأ: {e}")
        return

    # ===== 🔓 الخيار الثاني: iOS 9.0 حتى iOS 26.1 بدون شبكة =====
    elif cd == "iphone_legacy_bypass":
        try: bot.answer_callback_query(call.id)
        except: pass
        
        text = (
            "🔓 **iOS 9.0 حتى iOS 26.1 (بدون شبكة)**\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "📌 **المميزات:**\n"
            "• تجاوز قفل تفعيل iCloud غير متصل مجاناً (A5-A12+).\n"
            "• الإقلاع السريع - ميزة بدء التشغيل السريع لتجاوز التمرير.\n"
            "• تجاوز MDM مجاني مع دعم الإغلاق.\n"
            "• تفعيل رمز المرور - الأدوات الكاملة متوفرة مجاناً.\n"
            "• مفعل CheckM8 Hello لأجهزة A9-A11 (مجاني).\n"
            "• قم بتعطيل تحديثات OTA وأدوات منع إعادة ضبط المصنع.\n"
            "• دعم كامل لمتجر آبل والإشعارات بعد التفعيل.\n"
            "━━━━━━━━━━━━━━━━━━"
        )
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("📥 رابط الأداة", url="https://mega.nz/file/gns1CTYA#Qq4PigKzpZ2INjLMZAbY-7nC26i0Q-7tmTKYRoMfhzU"),
            types.InlineKeyboardButton("📝 موقع رفع السيريال", url="https://iunlock.cloud/register"),
            types.InlineKeyboardButton("🔙 العودة للقائمة السابقة", callback_data="iphone_bypass_menu")
        )
        
        try:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        except Exception as e:
            print(f"❌ خطأ: {e}")
        return

    # 📱 3. معالج ملفات إصدار iOS 18.3.1 المستخرج بالكامل من الصورة الأولى
    elif cd == "ipcc_ios_18_3_1":
        try:
            bot.answer_callback_query(call.id)
            if 'track_tool' in globals():
                track_tool("عرض ملفات IPCC 18.3.1", call.message.chat.id)
                
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(
                types.InlineKeyboardButton("📥 تحميل لـ كل موديلات 11", url="https://www.mediafire.com/file/9eghuofz93joja2/IP_11Xxx_ios18.3.1_ALLUNLOCKER.COM.ipcc/file"),
                types.InlineKeyboardButton("📥 تحميل لـ كل موديلات 12", url="https://www.mediafire.com/file/ci6j3vhi4a4441q/IP_12Xxx_ios_18.3.1_ALLUNLOCKER.COM.ipcc/file"),
                types.InlineKeyboardButton("📥 تحميل لـ (XS / XS Max / XR / SE 2020)", url="https://www.mediafire.com/file/4yun2atxg0l0vbk/IP_XS%252CXR%252CMax_ios_18.3.1_ALLUNLOCKER.COM.ipcc.ipcc/file"),
                types.InlineKeyboardButton("🇨🇳 الملف الصيني لـ (XS / Max / XR / SE 2020)", url="https://www.mediafire.com/file/vvf9ke2y6t5khem/IP_XS%252CXR%252CMax_4G_ios18.3.1_China.ipcc/file"),
                types.InlineKeyboardButton("🇨🇳 الملف الصيني لـ كل إصدارات آيفون 11", url="https://www.mediafire.com/file/1o1pyiv5q5gg833/iP_11Xxx_4G_ios18.3.1_China.ipcc/file"),
                types.InlineKeyboardButton("🔙 رجوع للقائمة", callback_data="iphone_unlock_ipcc")
            )
            
            display_text = (
                "#ملفات #الشبكة للآيفون الاصدار iOS 18.3.1\n"
                "يمن موبايل #CDMA 📲\n\n"
                "📋 **روابط التحميل المتاحة للأجهزة:**\n"
                "• لـ كل موديلات 11 و 12 والموديلات القديمة الحصرية.\n\n"
                "💡 **الافضل استخدام #الملفات #الصينية**\n"
                "⚠️ ملفات ايفون 13 مش شعاله ❌ لذلك لم اقم بارفاقها.\n\n"
                "م/ عادل بن شعيب"
            )
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=display_text,
                reply_markup=markup,
                parse_mode="Markdown",
                disable_web_page_preview=True
            )
        except Exception as e:
            print(f"❌ خطأ في قسم ipcc_ios_18_3_1: {e}")
        return

    # 🔥 4. معالج ملفات إصدار iOS 18.4 & 18.4.1 (شامل ملف آيفون 13 الجديد وملف الحذف)
    elif cd == "ipcc_ios_18_4_1":
        try:
            bot.answer_callback_query(call.id)
            if 'track_tool' in globals():
                track_tool("عرض ملفات IPCC 18.4.1", call.message.chat.id)
                
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(
                types.InlineKeyboardButton("📥 ملف آيفون 11 و 12 (شغال تمام) ☑️", url="https://www.mediafire.com/file/35xfuy8ls7n56i7/All_iPhones_ios18.4_ALLUNLOCKER.COM.ipcc/file"),
                types.InlineKeyboardButton("🔥 ملف آيفون 13 الجديد الشامل لـ 18.4.1 🚀", url="https://www.mediafire.com/file/0irycqxozf7cdqi/iPhone_13_All.ipcc/file"),
                types.InlineKeyboardButton("📱 ملف آيفون 13 الاحتياطي (إصدار 18.4 سابق) 👍", url="https://www.mediafire.com/file/05k362jgcgwahzw/ipcc_for_iphone_13.ipcc/file"),
                types.InlineKeyboardButton("🛠️ ملف الحذف المباشر لفك التعليق Remove IPCC 💨", url="https://www.mediafire.com/file/lmne4fsy1yx9399/Remove.ipcc/file"),
                types.InlineKeyboardButton("🔙 رجوع للقائمة", callback_data="iphone_unlock_ipcc")
            )
            
            display_text = (
                "#ملف شبكة جديد 🔥 لايفونات 13 بشكل عام 📱\n"
                "يدعم الاصدار الاخير 18.4.1\n"
                "وايضاً يدعم الاصدار 18.4 ✅\n"
                "بدون تهنيج / بدون تعليق ✅\n"
                "الملف طبعاً لثبات التغطية 📶 بدون الاتصال 911\n\n"
                "⚠️ **توضيحات هامة جداً:**\n"
                "1️⃣ طبعاً لما تقول ثبات تغطية معناه بتستخدم ملف امريكي عبر الكود و شريحة الكترونية و شريحة فرايزون كما تم شرحه سابقاً في القناة ☝️\n"
                "2️⃣ و #الملف #السابق ايضاً شغال على الاصدار الاخير 18.4.1 ومجرب 👌 استخدمه في حالة واجهت مشكلة مع هذا الملف الجديد.\n"
                "3️⃣ تمت #تجربة هذه الملفات لـ ايفون 11 و 12 وشغاله تمام ماتعلق ☑️\n\n"
                "💡 **الذي واجه مشكلة بحذف الملف وتعليق الايفون:**\n"
                "يقوم بإخراج الشريحة وعمل اعادة تشغيل للايفون وعمل وضع الطيران مباشرة عشان مايبعلق عليك الجهاز ثم قم بحذف الملف باستخدام ملف الحذف المرفق بالأزرار، او عبر الادوات واختيار Remove IPCC.\n\n"
                "م/ عادل بن شعيب"
            )
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=display_text,
                reply_markup=markup,
                parse_mode="Markdown",
                disable_web_page_preview=True
            )
        except Exception as e:
            print(f"❌ خطأ في قسم ipcc_ios_18_4_1: {e}")
        return

    # ===== 🔌 الدليل الرئيسي: قطع الآيفون PWN =====
    elif cd == "iphone_pwn_parts":
        try: bot.answer_callback_query(call.id)
        except: pass
        
        display_text = (
            "📖 **دليل شامل ومختصر حول التعامل مع قطع إدخال أجهزة iPhone في وضع Pwned DFU (ثغرة checkm8):**\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "1️⃣ **كابل / أداة MAGICO MANGO DFU:**\n"
            "قطعة مخصصة لإدخال أجهزة Apple (من معالجات A7 حتى A11) في وضع DFU بضغطة زر وتسهيل تنفيذ ثغرة checkm8/PWN.\n\n"
            "🔌 *طريقة التوصيل:*\n"
            "• منفذ USB-A يُربط مباشرة بالكمبيوتر (يفضل منفذ أصلي دون موزع USB لتجنب انقطاع التوافق).\n"
            "• منفذ Lightning يُربط بجهاز الآيفون مباشرة.\n\n"
            "🔄 *إعادة التهيئة والتحديث (Firmware Update):*\n"
            "• يتم عبر أداة الشركة الرسمية (Magico Tool أو أداة الترقية الخاصة بها لنظام Windows).\n"
            "• اضغط باستمرار على زر الوضع في القطعة أثناء توصيلها بالكمبيوتر للتعرف عليها كـ Bootloader لتحديث البرنامج الثابت.\n\n"
            "🛠️ *إصلاح المشاكل الشائعة:*\n"
            "• الجهاز لا يدخل الوضع: تحقق من سلامة كابل Lightning ونظافة منفذ الشحن في الهاتف.\n"
            "• الكمبيوتر لا يتعرف على القطعة: أعد تثبيت تعريفات LibUSB أو CH340/FTDI حسب الشريحة الداخلية.\n\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            "2️⃣ **لوحة التطوير RP2350 / RP2040 (المشار إليها بـ RP2354A):**\n"
            "لوحة متحكم دقيق قائمة على معالجات Raspberry Pi RP-series مبرمجة لتنفيذ هجوم ثغرة checkm8 المستقل (Standalone Pwned DFU).\n\n"
            "🔌 *مخطط التوصيلات:*\n"
            "• مدخل الطاقة والتحكم (USB Type-C): يُوصل بالشاحن أو الكمبيوتر لتغذية اللوحة.\n"
            "• مخرج الهاتف (USB Host): يتطلب توصيل منفذ USB A (أو كابل OTG) المتصل بأرجل USB Host لربط الآيفون بكابل Lightning أصلي.\n\n"
            "🔄 *تركيب النظام والفرمطة (Flashing Firmware):*\n"
            "• اضغط باستمرار على زر BOOTSEL في اللوحة أثناء توصيلها بالكمبيوتر عبر منفذ Type-C (ستظهر كوحدة تخزين RPI-RP2).\n"
            "• لفرمطة الذاكرة بالكامل: انسخ ملف `flash_nuke.uf2` وأسقطه داخل المجلد، وستتم إعادة التشغيل تلقائياً.\n"
            "• لتثبيت نظام PWN: أعد الدخول لوضع BOOTSEL واسحب ملف البايلود بصيغة `.uf2` المخصص للـ Pwned DFU.\n\n"
            "🛠️ *حل الأعطال:*\n"
            "• فشل تنفيذ الثغرة (Exploit Failed): تأكد من جودة كابل Lightning، وجرب إعادة تشغيل اللوحة بزر RESET بعد إدخال الهاتف في وضع DFU العادي.\n"
            "━━━━━━━━━━━━━━━━━━"
        )
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🔌 قطعة MAGICO MANGO DFU V1", callback_data="pwn_magico_mango"),
            types.InlineKeyboardButton("⚡ قطعة RP2354A Firmware", callback_data="pwn_rp2354a"),
            types.InlineKeyboardButton("🛠️ برنامج شامل لجميع القطع PWN", callback_data="pwn_all_in_one"),
            types.InlineKeyboardButton("🔙 العودة لقسم الآيفون", callback_data="main_iphone")
        )
        
        try:
            bot.edit_message_text(display_text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        except Exception as e:
            print(f"❌ خطأ: {e}")
        return

    # ===== 1️⃣ الخيار الأول: قطعة MAGICO MANGO DFU V1 =====
    elif cd == "pwn_magico_mango":
        try: bot.answer_callback_query(call.id)
        except: pass
        
        display_text = (
            "🚫 **لا للاحتكار**\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "⚙️ **برمجة قطعة MAGICO MANGO DFU V1**\n"
            "🔐 كلمة سر فك الضغط: `321`\n\n"
            "كثير من الإخوة تلفت معهم القطعة سواء بسبب فيرموير خاطئ، أو أنها غير مبرمجة مصنعياً سهواً، أو بسبب سوء الاستخدام.\n\n"
            "وبما أن الفيرموير محتكر وأغلب المستخدمين يجهلون طريقة برمجة معالجات RASPBERRY، هذا هو الحل:\n\n"
            "📁 المجلد يحتوي على أداة `picotool` والفيرموير والأوامر:\n"
            "1. افتح المجلد وافتح موجه الأوامر (CMD).\n"
            "2. اكتب الأمر التالي:\n"
            "`picotool load firmware.bin -t bin -o 0x10000000`\n\n"
            "سيبدأ بتثبيت الفيرموير وترجع القطعة للعمل بفضل الله.\n"
            "🌹 كل الشكر للمهندس: **محمد رمضان (Mohamad Ramadan)**"
        )
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🖼️ صور الشرح", url="https://t.me/haithamMax1/1069"),
            types.InlineKeyboardButton("📥 رابط التنزيل", url="https://drive.google.com/drive/folders/1S3mxUolL46j6sP2s1KFE7cBs-UkUsPfL?usp=drive_link"),
            types.InlineKeyboardButton("🔙 رجوع لقائمة قطع PWN", callback_data="iphone_pwn_parts")
        )
        
        try:
            bot.edit_message_text(display_text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        except Exception as e:
            print(f"❌ خطأ: {e}")
        return

    # ===== 2️⃣ الخيار الثاني: قطعة RP2354A Firmware =====
    elif cd == "pwn_rp2354a":
        try: bot.answer_callback_query(call.id)
        except: pass
        
        display_text = (
            "⚡ **قطعة RP2354A Firmware**\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "تحميل الفيرموير والأدوات المخصصة لتحديث وبرمجة قطعة RP2354A مع الشرح بالفيديو:"
        )
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("📥 رابط التنزيل", url="https://drive.google.com/file/d/1hfgqgmoZxF-zgrcAjMt9hy-gJ5mpawd5/view?usp=drive_link"),
            types.InlineKeyboardButton("📺 شرح فيديو", url="https://youtu.be/jAv0QW_ApGs?si=fTTmU_lamha7DoYS"),
            types.InlineKeyboardButton("🔙 رجوع لقائمة قطع PWN", callback_data="iphone_pwn_parts")
        )
        
        try:
            bot.edit_message_text(display_text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        except Exception as e:
            print(f"❌ خطأ: {e}")
        return

    # ===== 🛠️ الخيار الثالث: برنامج شامل لجميع القطع PWN =====
    elif cd == "pwn_all_in_one":
        try: bot.answer_callback_query(call.id)
        except: pass
        
        display_text = (
            "🛠️ **برنامج شامل لجميع قطع PWN**\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "📋 **القطع واللوحات المدعومة:**\n"
            "• Waveshare RP2350 USB-A\n"
            "• Waveshare RP2350 Zero\n"
            "• Pimoroni TINY2350\n"
            "• Raspberry Pi Pico 2\n"
            "• Waveshare RP2350 (Dual USB-C)\n"
            "• Waveshare RP2350-Tiny *(Detect only)*\n"
            "• Raspberry Pi Pico (RP2040)\n"
            "• Adafruit Feather RP2040 *(Detect only)*\n\n"
            "🔐 **كلمة سر فك الضغط:** `HITHAMMAX`\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "📥 اضغط على الزر أدناه لبدء التنزيل:"
        )
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("📥 رابط التنزيل المباشر", url="https://drive.google.com/file/d/1BrnX0b3Ma5B0kZbvioWZ0502Fwgk4LXm/view?usp=drive_link"),
            types.InlineKeyboardButton("🔙 رجوع لقائمة قطع PWN", callback_data="iphone_pwn_parts")
        )
        
        try:
            bot.edit_message_text(display_text, call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        except Exception as e:
            print(f"❌ خطأ: {e}")
        return
    # ====================================================================================
    # 🗂️ [5] القائمة الفرعية الجديدة لقسم التعليمات (تضم الشروحات من تعليمات 1 إلى تعليمات 4)
    # ====================================================================================
    elif cd == "ipcc_important_instructions":
        try:
            bot.answer_callback_query(call.id)
            if 'track_tool' in globals():
                track_tool("قائمة التعليمات الشاملة IPCC", call.message.chat.id)
                
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(
                types.InlineKeyboardButton("🇨🇳 طريقة إضافة وتفعيل الملف الصيني الأصلي", callback_data="ipcc_inst_china"),
                types.InlineKeyboardButton("⚠️ تعليمات 1", callback_data="ipcc_inst_1"),
                types.InlineKeyboardButton("⚠️ تعليمات 2", callback_data="ipcc_inst_2"),
                types.InlineKeyboardButton("⚠️ تعليمات 3", callback_data="ipcc_inst_3"),
                types.InlineKeyboardButton("⚠️ تعليمات 4", callback_data="ipcc_inst_4"),
                types.InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="iphone_unlock_ipcc")
            )
            
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="⚠️ **قسم التعليمات الهامة وشروحات ثبات التغطية:**\n\nاضغط على أي خيار أدناه لقراءة الشرح التفصيلي والكود البرمجي الخاص بكل طريقة بالتفصيل ومباشرة:",
                reply_markup=markup,
                parse_mode="Markdown"
            )
        except Exception as e:
            print(f"❌ خطأ في قائمة التعليمات: {e}")
        return

    # 🇨🇳 شرح تفعيل الملف الصيني (المنشور الأصلي 603)
    elif cd == "ipcc_inst_china":
        try:
            bot.answer_callback_query(call.id)
            original_post = "https://t.me/AdelBinShuaib/603"
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(
                types.InlineKeyboardButton("🔗 رابط المنشور الأصلي في القناة", url=original_post),
                types.InlineKeyboardButton("🔙 رجوع لقسم التعليمات", callback_data="ipcc_important_instructions")
            )
            display_text = (
                "طريقة اضافة #الملف #الصيني 🇨🇳 لتشغيل يمن موبايل 📶 بعيداً عن الملفات العادية IPCC# لأجهزة #الآيفون 📱\n\n"
                "⚠️ **هذا المنشور ضمن شروحات برمجة الشريحة الالكترونية** 👩‍💻\n\n"
                "📌 **من مميزات الملف الصيني:**\n"
                "انه ماينحذف معك بالتحديث مثل الملفات العادية بتكون تحدّث أي تحديث جديد لنظام الـ iOS وكأنه معك شريحة VoLTE او GSM 😍😍 وبدون الخوف من فقدان التغطية 📶✔️\n\n"
                "⚙ *خطوات الإضافة البرمجية:*\n"
                "1️⃣ قم بشراء شريحة الكترونية خاصة بالايفون.\n"
                "2️⃣ يتم تركيب الشريحة الالكترونية فوق الشريحة الاساسية لـ يمن موبايل ويتم ادخالها في الجوال.\n"
                "3️⃣ ثم تظهر لك قائمة الضبط اختار: `5G Auto TMSI Mode` او `Auto TMSI Mode` *(وقد تجده ايضاً باسم Unlock mode)*\n"
                "4️⃣ ثم `Other` او `input imsi`.\n\n"
                "👇 *واذا ماظهرت لك قائمة الضبط تلقائياً:*\n"
                "تقوم بالذهاب إلى إعدادات الايفون 📱 ⬅ خلوي Cellular ⬅ تطبيقات الـ SIM أو SIM Applications.\n"
                "• ثم اختار ⬅ `Auto TMSI Mode`\n"
                "• ثم `Other` او `input imsi`\n"
                "• ونكتب الكود الصيني ☑: `4601100`\n"
                "• اختار ارسال Send ثم موافق Accept\n"
                "• ثم اختار ⬅ `CDMA Mode` او `CDMA 4G/5G Mode`.\n\n"
                "🔄 الآن قم بإخراج الشرائح وتركيب شريحة يمن موبايل فقط ثم شغل وضع الطيران ثواني وطفيه ثم اتصل 911 واغلق الاتصال فوراً، الان بتظهر تغطية الشبكة 📶 وببيانات 3G جاهزة وبثبات تام.\n\n"
                "⚠️ *ملاحظات هامة :-*\n"
                "• هذه الطريقة تنفع من اصدارات سلسة ايفون 12 ومادون ذلك للاجهزة الداعمة لـ CDMA 77.\n"
                "• اجهزة ايفون 12 تدعم هذا الملف الصيني 🇨🇳 لكن يجب ان تكون شريحة 77 الـ PRL برقم 63500 اي معدلة 5G.\n"
                "• ايفونات 13 لاتدعم هذا الملف وانما تدعم الملف الامريكي بشريحة معدلة.\n\n"
                "م/ عادل بن شعيب"
            )
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=display_text, reply_markup=markup, parse_mode="Markdown", disable_web_page_preview=True)
        except Exception as e:
            print(f"❌ خطأ في ipcc_inst_china: {e}")
        return

    # ⚠️ تعليمات 1: فحص رقم الـ PRL لآيفون 12
    elif cd == "ipcc_inst_1":
        try:
            bot.answer_callback_query(call.id)
            markup = types.InlineKeyboardMarkup(row_width=1).add(types.InlineKeyboardButton("🔙 رجوع لقسم التعليمات", callback_data="ipcc_important_instructions"))
            display_text = (
                "📢 **تعليمات 1 :-**\n\n"
                "#الملف حق ايفون 12 يشتغل مباشرة وتطلع التغطية 📶 اذا كانت شريحتك معدلة من قبل بدون استخدام شريحة #فرايزون ❌\n\n"
                "⚙️ **طريقة فحص الشريحة:**\n"
                "⬅️ اعدادات > عام > حول\n"
                "⬅️ شركة الاتصالات واضغط عليه مره يتلاقي تغير وظهر رقم PRL الخاص بالشريحة ☑️\n\n"
                "📊 **النتيجة والفحص:**\n"
                "• **اذا الرقم PRL 63500:** جاهز 👍 ضيف ملف الشبكة وبتطلع لك التغطية مباشرة، طبعاً بدون 3G ❌ (معاكم شبكات النت حق الشوارع بكل مكان 💀😂)، المهم الاتصال شغال مع الرسائل النصية.\n\n"
                "📌 أما الذي معه الملف الصيني 🇨🇳 من قبل مع 5G لن ينحذف الملف عليه بأي تحديث جديد والافضل تركيب هذا الملف عشان تحدّث وانت مرتاح 😎\n\n"
                "م/ عادل بن شعيب"
            )
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=display_text, reply_markup=markup, parse_mode="Markdown")
        except Exception as e:
            print(f"❌ خطأ في ipcc_inst_1: {e}")
        return

    # ⚠️ تعليمات 2: بخصوص مشكلة تعليق إصدار 18.4
    elif cd == "ipcc_inst_2":
        try:
            bot.answer_callback_query(call.id)
            markup = types.InlineKeyboardMarkup(row_width=1).add(types.InlineKeyboardButton("🔙 رجوع لقسم التعليمات", callback_data="ipcc_important_instructions"))
            display_text = (
                "📢 **تعليمات 2 :-**\n\n"
                "#بخصوص #مشكلة ملفات شبكة يمن موبايل على الاصدار الاخير 🔥❌ **iOS 18.4**\n\n"
                "• ايفون فئة 11 و 13 يعلقوا بعد تركيب الملف مباشرة بالايفون 📱\n"
                "• اما ايفون 12 مايعلق ☑️\n"
                "• #التهنيج بعد تركيب الملف مباشرة مايروح الا بحذف الملف ❌🗑️\n\n"
                "🛠️ **الحلول والبدائل المتاحة:**\n"
                "⬅️ ايفون 11 باستخدام الملف الصيني 🇨🇳 عبر الكود شغال تمام دون مشاكل 👌 بدل الملف X IPCC العادي.\n"
                "⬅️ بقية الموديلات الاخرى مثل XR و XS و XS Max لم تتم التجربة عليهم واذا جربت وعلق الجهاز قم بحذف الملف وتركيب الملف الصيني 🇨🇳👍\n\n"
                "⚠️ **ملاحظة:** الذي علق معه ايفون 12 بعد تركيب الملف يحذفه ويركب الملف الصيني مع شريحة معدلة 5G 👍\n\n"
                "م/ عادل بن شعيب"
            )
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=display_text, reply_markup=markup, parse_mode="Markdown")
        except Exception as e:
            print(f"❌ خطأ في ipcc_inst_2: {e}")
        return

    # ⚠️ تعليمات 3: ثبات تغطية آيفون 13 بدون 911 (هدية الاخ عادل بن شعيب)
    elif cd == "ipcc_inst_3":
        try:
            bot.answer_callback_query(call.id)
            markup = types.InlineKeyboardMarkup(row_width=1).add(types.InlineKeyboardButton("🔙 رجوع لقسم التعليمات", callback_data="ipcc_important_instructions"))
            display_text = (
                "📢 **تعليمات 3 :-**\n\n"
                "🔥 #رمضان #هدية | ننشر لكم طريقة ثبات التغطية بدون 911 📶📲☑️ في ايفونات 13 بالاصدار 18 و 26\n\n"
                "⚙️ **الطريقة والخطوات بالتفصيل:**\n"
                "1️⃣ تسوي ملف من الاداة حق ايفون 13 شفته طلعت طوارئ.\n"
                "2️⃣ وبعدين اعمل طريقة الفرايزون: دخل يمن موبايل قديم واتصل 911 وخرجها وركب فرايزون وعيد تشغيل اجباري وبعدين ركب يمن موبايل قديم ثواني وخرجها.\n"
                "3️⃣ وبعدين خلاص جيب شريحه الزبون وركبها مع الالكتروني وسوي هذا الكود البرمجي: `3101301`\n\n"
                "📊 **النتيجة والمميزات:**\n"
                "• مافيش داعي تحول الشريحة 5G 🚫\n"
                "• ويشتغل معك مباشرة التغطية بدون ماتتصل 911\n"
                "• مع الـ 3G والبت 👍\n"
                "• واصبحت التغطية ثابته حتى بعد عمل اعادة تشغيل للايفون 📱\n\n"
                "م/ عادل بن شعيب & Ashraf-Soft"
            )
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=display_text, reply_markup=markup, parse_mode="Markdown")
        except Exception as e:
            print(f"❌ خطأ في ipcc_inst_3: {e}")
        return

    # ⚠️ تعليمات 4: تفعيل الآيفون على شركة USA Xfinity
    elif cd == "ipcc_inst_4":
        try:
            bot.answer_callback_query(call.id)
            markup = types.InlineKeyboardMarkup(row_width=1).add(types.InlineKeyboardButton("🔙 رجوع لقسم التعليمات", callback_data="ipcc_important_instructions"))
            display_text = (
                "📢 **تعليمات 4 :-**\n\n"
                "📲 تفعيل الايفون ⬅️ **USA Xfinity** على شركة شريحة يمن موبايل نظام CDMA# 🔥\n\n"
                "📊 **حالة التغطية والأنظمة:**\n"
                "• يشتغل ⬅️ اتصال مع بيانات 3G 📶\n"
                "• ابتداءً من ايفون XS و XR الى ايفون فئة 12 المغلق والمشفر على هذه الشركة الامريكية.\n"
                "• من ايفون 13 ومافوق على شرائح نظام **#VoLTE**.\n\n"
                "⚙️ **#التفعيل #طريقة:**\n"
                "عن طريق الملف الصيني 🇨🇳 عبر الكود `4601100` يتم اضافة ملف التغطية من شريحة الكترونية اخرى غير الشريحة الالكترونية الاساسية التي يتم اضافة كود الشركة منها عبر الكود `2040400`.\n\n"
                "💡 **بمعنى أوضح:** ضيف الملف الصيني من شريحة الكترونية، ثم قم بإخراجها وتركيب شريحة الكترونية اخرى جديدة وقم بإضافة كود الشركة المغلق عليه الايفون وسوف يتم التنشيط بنجاح وظهور التغطية 👌💯\n\n"
                "م/ عادل بن شعيب"
            )
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=display_text, reply_markup=markup, parse_mode="Markdown")
        except Exception as e:
            print(f"❌ خطأ في ipcc_inst_4: {e}")
        return


    # 🔥 هنا تضع الأكواد الجديدة بالظبط وبنفس أبعاد المسافات:
    elif cd == "btn_iphone_5s_x" or cd == "iphone_5s_x":
        try: bot.answer_callback_query(call.id)
        except: pass
        # استدعاء دالة الانتظار فوراً وتمرير اسم القسم
        request_s_unlocker(call.message, "iPhone 5s to X (iOS 14-17)")
        return

    elif cd == "btn_iphone_xr_17pm" or cd == "iphone_xr_17pm":
        try: bot.answer_callback_query(call.id)
        except: pass
        # استدعاء دالة الانتظار فوراً وتمرير اسم القسم
        request_s_unlocker(call.message, "XR to 17 Pro Max (iOS 18.6-26.1)")
        return

   
    # ===== 🎁 قسم الأدوات المجانية (الشامل) ====
    elif cd == "main_free_tools":
        try: bot.answer_callback_query(call.id)
        except: pass
        
        try:
            # 🌟 تم تعديل العرض هنا ليكون (1) أي زر واحد بعرض الشاشة لكل سطر
            markup = types.InlineKeyboardMarkup(row_width=1)
            
            markup.add(
                types.InlineKeyboardButton("🌐 Server 1", callback_data="free_server1"),
                types.InlineKeyboardButton("🌐 IDM مجاناً", callback_data="free_idm_tool"),
                types.InlineKeyboardButton("🟢 فك حظر واتساب", callback_data="whatsapp_unban_tool"),
                types.InlineKeyboardButton("📱 App Manager", callback_data="page_free_android_app_manager"),
                types.InlineKeyboardButton("⚡ Network Control", callback_data="page_free_android_ultimate_network"),
                types.InlineKeyboardButton("🛠️ Samfw tool", callback_data="link_free_android_samfw"),
                types.InlineKeyboardButton("✨ MaxTech VIP", callback_data="page_free_android_maxtech_vip"),
                types.InlineKeyboardButton("📲 نقل هاتف", callback_data="page_free_android_mobimover"),
                types.InlineKeyboardButton("🌐 سايفون VPN", callback_data="page_free_android_psiphon_vpn"),
                types.InlineKeyboardButton("🛡️ إيقاف مكافح الفيروسات", callback_data="link_free_android_defender_control"),
                types.InlineKeyboardButton("💻 Activator Master", callback_data="link_free_android_activator_master"),
                types.InlineKeyboardButton("🕵️ Mysterious-Dev", callback_data="page_free_android_mysterious_dev"),
                types.InlineKeyboardButton("🔍 قراءة معلومات أجهزة الهونر بوضع الفاست بوت Honor", callback_data="link_free_android_honor_fastboot"),
                types.InlineKeyboardButton("🛠️ 3uTools V3.28", callback_data="link_free_iphone_3utools_v3_28"),
                types.InlineKeyboardButton("🚀 3uTools الأخير", callback_data="link_free_iphone_3utools_latest"),
                types.InlineKeyboardButton("🍏 iTunes 12.13.9", callback_data="link_free_iphone_itunes_12_13_9"),
                types.InlineKeyboardButton("💾 نسخة احتياطية من الملفات والنظام بأكمله", callback_data="free_acronis_backup"),
                types.InlineKeyboardButton("🏠 العودة للرئيسية", callback_data="back_start")
            )
            
            bot.edit_message_text(
                "🎁 **قسم الأدوات المجانية الشامل:**\nجميع الأدوات الحصرية والمجانية للأندرويد، الآيفون، والكمبيوتر مجمعة لك هنا في مكان واحد لسهولة الوصول السريع:",
                call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown"
            )
        except Exception as e:
            print(f"❌ خطأ في فتح قسم الأدوات المجانية الشامل: {e}")
        return
    elif cd == "whatsapp_unban_tool":
        track_tool("أداة فك حظر واتساب", user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("📥 رابط تحميل الأداة",
                url="https://mega.nz/file/VRM00TgD#cu0R1eaDrzeGlz0Mn-AsXIcQGsA0CtrsYIZhltb-9ag"),
            types.InlineKeyboardButton("🎬 فيديو تعليمي",
                url="https://youtu.be/HENsWi2N3Oo?si=PYFFnCacWUe3ONDV"),
            types.InlineKeyboardButton("🔙 رجوع", callback_data="main_free_tools"),
        )
        bot.edit_message_text(
            "🟢 **أداة فك حظر واتساب:**",
            user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown"
        )

    elif cd == "free_cat_android":
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("📲 نقل هاتف",      callback_data="page_free_android_mobimover"),
            types.InlineKeyboardButton("🛠️ Samfw tool",    callback_data="link_free_android_samfw"),
        )
        markup.add(
            types.InlineKeyboardButton("✨ MaxTech VIP",    callback_data="page_free_android_maxtech_vip"),
            types.InlineKeyboardButton("🕵️ Mysterious-Dev", callback_data="page_free_android_mysterious_dev"),
        )
        markup.add(
            types.InlineKeyboardButton("🔍 قراءة معلومات الهونر فاست بوت", callback_data="link_free_android_honor_fastboot"),
        )
        markup.add(
            types.InlineKeyboardButton("🛡️ إيقاف مكافح الفيروسات", callback_data="link_free_android_defender_control")
        )
        markup.add(
            types.InlineKeyboardButton("💻 أدوات تفعيل الويندوز وإيقاف الـ Update", callback_data="link_free_android_activator_master")
        )
        markup.add(
            types.InlineKeyboardButton("🌐 سايفون Psiphon VPN", callback_data="page_free_android_psiphon_vpn")
        )
        # 🌟 الأزرار الجديدة المضافة والموزونة بالملي 🌟
        markup.add(
            types.InlineKeyboardButton("📱 App Manager", callback_data="page_free_android_app_manager"),
            types.InlineKeyboardButton("⚡ Ultimate Network Control", callback_data="page_free_android_ultimate_network")
        )
        markup.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="main_free_tools"))
        bot.edit_message_text(
            "🤖 **أدوات أندرويد مجانية:**",
            user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown"
        )

    elif cd == "free_cat_iphone":
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("🛠️ 3utools V3.28",  callback_data="link_free_iphone_3utools_v3_28"),
            types.InlineKeyboardButton("🚀 3utools الأخير", callback_data="link_free_iphone_3utools_latest"),
        )
        markup.add(
            types.InlineKeyboardButton("🍏 iTunes 12.13.9 (64-bit)", callback_data="link_free_iphone_itunes_12_13_9")
        )
        markup.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="main_free_tools"))
        bot.edit_message_text(
            "📱 **أدوات آيفون مجانية:**",
            user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown"
        )
        
    elif cd == "page_free_android_mobimover":
        track_tool("برنامج نقل من هاتف لآخر", user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("📥 تحميل البرنامج", url=DATA["free_android"]["mobimover"][1]),
            types.InlineKeyboardButton("🔙 رجوع",           callback_data="free_cat_android"),
        )
        bot.edit_message_text(
            hmaxi18n.translate_static_content("mobimover", MOBIMOVER_DESC, hmaxi18n.get_language(user_id)),
            user_id, call.message.message_id,
            reply_markup=markup, parse_mode="Markdown"
        )

    elif cd == "page_free_android_maxtech_vip":
        track_tool("MaxTech VIP", user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("📥 تحميل MaxTech VIP", url=DATA["free_android"]["maxtech_vip"][1]),
            types.InlineKeyboardButton("🔙 رجوع",              callback_data="free_cat_android"),
        )
        bot.edit_message_text(
            hmaxi18n.translate_static_content("maxtech_vip", MAXTECH_VIP_DESC, hmaxi18n.get_language(user_id)),
            user_id, call.message.message_id,
            reply_markup=markup, parse_mode="Markdown"
        )

    # ===== 🕵️ أداة Mysterious-Dev =====
    elif cd in ["page_free_android_mysterious_dev", "link_free_android_mysterious_dev", "link_tools_mysterious_dev", "mysterious_dev"]:
        try: bot.answer_callback_query(call.id)
        except: pass
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        
        # ضع رابط التحميل الحقيقي هنا
        markup.add(types.InlineKeyboardButton("📥 تحميل الأداة", url="https://link-to-download.com"))
        
        # 🌟 تم تصحيح الوجهة هنا لتعود للقائمة الصحيحة مباشرة
        markup.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="main_free_tools"))
        
        display_text = (
            "🕵️ **أداة Mysterious-Dev:**\n\n"
            "أداة قوية ومتميزة في مجال التعامل مع أجهزة الأندرويد والعمليات البرمجية الدقيقة.\n\n"
            "🔑 **معلومات التفعيل:**\n"
            "إليكم الرقم السري (Access Code) الذي يطلبه البرنامج بعد التثبيت:\n\n"
            "`1499c38f6765c0608fa573e972bea22e`\n\n"
            "📌 *اضغط على الكود أعلاه للنسخ التلقائي.*"
        )
        
        bot.edit_message_text(
            display_text, call.message.chat.id, call.message.message_id, 
            reply_markup=markup, parse_mode="Markdown"
        )
        return

    # 🌐 معالج أداة سايفون Psiphon VPN المضافة حديثاً
    elif cd == "page_free_android_psiphon_vpn":
        track_tool("برنامج سايفون VPN", user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("📥 تحميل سايفون Psiphon VPN", url="https://www.mediafire.com/file/e75qx3oap8c70fc/VPN-Psiphon.rar/file"),
            types.InlineKeyboardButton("🔙 رجوع",           callback_data="free_cat_android"),
        )
        psiphon_desc = (
            "🌐 **برنامج سايفون تصفح آمن وكسر الحجب - Psiphon VPN**\n"
            "النسخة المستقرة والقوية لتأمين الاتصال وتخطي حظر المواقع والخدمات بكل سهولة 🚀\n\n"
            "✨ **أبرز مميزات البرنامج:**\n"
            "• تخطي الحجب الجغرافي والوصول إلى كافة المواقع المحظورة بنجاح\n"
            "• تشفير كامل لحركة مرور الإنترنت لحماية خصوصيتك وبياناتك الشخصية\n"
            "• اتصالات مستقرة وسريعة مع سيرفرات متعددة حول العالم\n"
            "• واجهة استخدام بسيطة وسهلة للغاية تعمل بضغطة زر واحدة\n"
            "• متوافق ومستقر تماماً وبدون أي تعقيدات في التشغيل\n\n"
            "📊 **تفاصيل الملف:**\n"
            "· اسم الملف: VPN-Psiphon.rar\n"
            "· منطقة الرفع: اليمن\n"
            "· الحالة: مجاني وجاهز للتشغيل مباشرة"
        )
        bot.edit_message_text(
            psiphon_desc, user_id, call.message.message_id,
            reply_markup=markup, parse_mode="Markdown"
        )

                

    # 📱 معالج أداة App Manager المضافة حديثاً
    elif cd == "page_free_android_app_manager":
        track_tool("برنامج App Manager", user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("📥 تحميل App Manager مباشرة", url="https://www.mediafire.com/file/pqrfqni4gb3j98y/AppManager.exe/file/"),
            types.InlineKeyboardButton("🔙 رجوع",           callback_data="free_cat_android"),
        )
        app_manager_desc = (
            "🖥️ **أداة إدارة التطبيقات - App Manager**\n"
            "🔥 **التحديث الجديد والأخير (الإصدار 1.2)** 🔥\n\n"
            "✨ **ما الجديد في هذا التحديث:**\n"
            "• تمت إضافة إمكانية تثبيت تطبيقات XAPK\n"
            "• تمت إضافة إمكانية النسخ الاحتياطي لتطبيق من هاتفك\n"
            "• تم إصلاح العديد من الأخطاء السابقة\n"
            "• تم إصلاح مشكلة في قراءة بعض التطبيقات\n"
            "• تمت إضافة عرض معلومات SDK وتاريخ حماية النظام في قسم 'المعلومات'\n"
            "• تحسينات عامة وإعادة تنظيم للواجهة\n\n"
            "📊 **تفاصيل الملف:**\n"
            "· اسم الملف: AppManager.exe\n"
            "· الحجم: 17.37 ميجابايت\n"
            "· تاريخ الرفع: 15 مارس 2026\n"
            "· منطقة الرفع: اليمن\n\n"
            "━━━━━━━━━━━━━━━━━\n\n"
            "📋 **المميزات والتفاصيل الأساسية للبرنامج:**\n\n"
            "⬛ **قسم قراءة التطبيقات:**\n"
            "1 - عرض جميع التطبيقات\n"
            "2 - عرض تطبيقات النظام\n"
            "3 - عرض التطبيقات المعطلة والمفعلة\n"
            "4 - عرض التطبيقات المثبتة من طرف ثالث\n"
            "5 - عرض التطبيقات المحذوفة\n\n"
            "⚙️ **قسم إدارة التطبيقات:**\n"
            "1 - تعطيل التطبيقات\n"
            "2 - تفعيل التطبيقات\n"
            "3 - حذف التطبيقات\n"
            "4 - مسح بيانات التطبيق\n"
            "5 - إيقاف التطبيق بالقوة\n"
            "6 - إخفاء التطبيقات وإظهارها\n\n"
            "📦 **قسم تثبيت التطبيقات:**\n"
            "1 - تثبيت تطبيقات APK\n"
            "2 - تثبيت تطبيقات APK ( وضع القوة )\n"
            "• **يدعم تثبيت عدة تطبيقات وبسرعة ممتازة**\n\n"
            "🔍 **قسم عرض التطبيق النشط:**\n"
            "1 - الحصول على باكج التطبيق النشط مع الاكتفيتي\n\n"
            "➡️ يدعم حتى أندرويد 16\n"
            "➡️ إمكانية ربط الهاتف عن طريق الواي فاي\n"
            "➡️ سرعة في الاداء ودقة في التنفيذ"
        )
        bot.edit_message_text(
            app_manager_desc, user_id, call.message.message_id,
            reply_markup=markup, parse_mode="Markdown"
        )

    # ⚡ معالج أداة Ultimate Network Control المضافة حديثاً
    elif cd == "page_free_android_ultimate_network":
        track_tool("أداة Ultimate Network Control", user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("📥 تحميل الأداة من سيرفر MEGA", url="https://www.mediafire.com/file/uuy8x5k128vvbak/Ultimate-Network-Control-V2-2.0.zip/file"),
            types.InlineKeyboardButton("🔙 رجوع",                callback_data="free_cat_android"),
        )
        network_control_desc = (
            "⚡ **أداة Ultimate Network Control - الإصدار المطور** ⚡\n\n"
            "هل تعاني من بطء الإنترنت أثناء العمل؟ أو استهلاك موارد الجهاز والرامات بسبب تحديثات ويندوز والبرامج المفاجئة؟ 🤔\n"
            "لقد تم تطوير أداة **Ultimate Network Control** لتمنحك التحكم الكامل في خدمات الشبكة وتحديثات النظام بضغطة زر واحدة! 💻🚀\n\n"
            "🛡️ **أبرز مميزات الأداة:**\n"
            "🚀 **وضع الأداء الأقصى (Max Performance):** إيقاف فوري لجميع الخدمات التي تستهلك الشبكة والمعالج في الخلفية `(BITS, Dosvc, Windows Update)` لضمان أقل \"بنج\" `(Ping)` ممكن أثناء العمل.\n"
            "🧹 **تنظيف شامل (System Cache):** خيار مخصص لمسح مخلفات النظام، ملفات التمب `(Temp)`، وتفريغ سلة المحذوفات لتسريع استجابة الجهاز.\n"
            "🚫 **السيطرة على المتصفحات:** منع تحديثات المتصفحات الإجبارية `(Edge, Chrome)` الإجبارية التي تبطئ التصفح والتحميل.\n"
            "🔄 **استعادة النظام:** ميزة العودة للوضع الافتراضي للويندوز في أي وقت بضغطة زر واحدة بكل أمان.\n"
            "🎨 **واجهة احترافية:** تصميم \"ASCII Art\" كلاسيكي مع تحكم سهل وبسيط لا يحتاج لخبرة برمجية.\n\n"
            "💡 **لماذا تستخدم هذه الأداة؟**\n"
            "ببساطة، لأن الويندوز يعمل دائماً خلف ظهرك ويستهلك سرعة الإنترنت الخاصة بك لتحميل ملفات وتحديثات لا تحتاجها الآن. هذه الأداة تضع \"المقود\" في يدك أنت! 🎮🔥\n"
            "*ملاحظة: الأداة آمنة تماماً، ومبرمجة بلغة Batch لتكون خفيفة ولا تحتاج للتثبيت.*\n\n"
            "👤 **المطور:** Developed By: Mohammed Alqadri\n\n"
            "⚠️ *ملحوظة:* انا غير مسؤول اذا لم تقم بتشغيل التحديثات كل فتره لان التحديثات ضروريه بالنظام."
        )
        bot.edit_message_text(
            network_control_desc, user_id, call.message.message_id,
            reply_markup=markup, parse_mode="Markdown"
        )

    elif cd == "link_free_android_samfw":
        try: bot.answer_callback_query(call.id)
        except: pass
        
        # 🌟 الرابط المحدث للإصدار v6.0.1
        url = "https://samfw.com/SamFwToolSetup_v6.0.1.zip"
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("📥 تحميل SamFw Tool v6.0.1", url=url),
            types.InlineKeyboardButton("🔙 رجوع", callback_data="main_free_tools")
        )
        
        bot.edit_message_text(
            "🛠️ **SamFw Tool v6.0.1:**\n\n"
            "تم تحديث الأداة إلى آخر إصدار. يمكنك تحميلها مباشرة عبر الزر أدناه.",
            call.message.chat.id, call.message.message_id, 
            reply_markup=markup, parse_mode="Markdown"
        )
        return


    # ===== أداة DFT Pro =====
    elif cd == "link_tool_dft_pro": # (تأكد من اسم الـ callback_data لديك)
        try: bot.answer_callback_query(call.id)
        except: pass
        
        url_dft = "https://www.mediafire.com/file/m4ssk83p5wr5mxa/DFTPRO_v8.0.0.exe/file"
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("📥 تحميل DFT Pro v8.0.0", url=url_dft),
            types.InlineKeyboardButton("🔙 رجوع", callback_data="main_tools") # تأكد من زر الرجوع المناسب
        )
        
        bot.edit_message_text(
            "🛠️ **أداة DFT PRO (الإصدار v8.0.0):**\n\n"
            "تم تحديث رابط الأداة لأحدث إصدار. اضغط على الزر أدناه للتحميل المباشر:",
            call.message.chat.id, call.message.message_id, 
            reply_markup=markup, parse_mode="Markdown"
        )
        return

    # ===== 🌐 أداة IDM المجانية =====
    elif cd == "free_idm_tool":
        try: bot.answer_callback_query(call.id)
        except: pass
        
        # تتبع الأداة لإضافتها في سجل الفني (إذا كانت الدالة موجودة)
        if 'track_tool' in globals():
            track_tool("أداة IDM Freezer & Activator", user_id)
            
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("📥 تحميل الأداة المباشر (Mediafire)", url="https://www.mediafire.com/file/mqzcpgbzcy8k7hg/IDM_Tool_V1.5.rar/file"),
            types.InlineKeyboardButton("🔙 رجوع لقسم الأدوات المجانية", callback_data="main_free_tools")
        )
        
        idm_desc = (
            "🌐 **أداة IDM Freezer & Activator مجاناً:**\n"
            "من المطور المبدع: **Ali Sakkaf**\n\n"
            "هدفها يريحك نهائياً من مشاكل داونلود مانجر (IDM) ورسالة \"السيريال مزيف\" المزعجة وتغنيك تماماً عن الكراكات والباتشات المفيرسة ومجهولة المصدر.\n\n"
            "برنامج نظيف وخفيف جداً وخالي من الفيروسات تماماً 🛡️\n\n"
            "✨ **المميزات الأساسية | Key Features:**\n"
            "1️⃣ **فحص الحالة الذكي (Status Check):** الأداة بتتعرف تلقائياً على حالة IDM في جهازك ومساره وتفاصيل التسجيل بضغطة زر.\n"
            "2️⃣ **تجميد الفترة التجريبية (Freeze Trial):** `[الخيار المستحسن والافضل]` بضغطة زر يوقف عداد الـ 30 يوم المجانية للأبد بدون استخدام أي سيريال وهمي، يعني مستحيل تطلع لك رسالة \"مزيف\" وتقدر تحدث البرنامج براحتك وأنت مرتاح.\n"
            "3️⃣ **التفعيل الكامل (Full Activation):** يسجل البرنامج باسمك، ويستخدم طريقتين مدمجة (تسجيل الريجستري + حقن الذاكرة DLL) عشان يمنع البرنامج من اكتشاف التفعيل ويخفي النوافذ المزعجة تماماً.\n"
            "4️⃣ **التنظيف العميق (Factory Reset):** يمسح أي كراكات قديمة أو قيم تالفة في الريجستري ويرجع لك IDM وكأنه جديد (وضع المصنع).\n\n"
            "⚠️ **تنويه هام / Important Note:**\n"
            "الأداة لا تحمل أو توزع أي نسخ مكركة! يجب عليك تحميل وتثبيت النسخة الرسمية والأصلية من موقع IDM أولاً لكي تعمل الأداة بشكل صحيح. `يرجى تشغيل البرنامج كمسؤول (Run as Administrator)` ليعمل بنجاح.\n\n"
            "🛑 **إخلاء مسؤولية / Disclaimer:**\n"
            "البرنامج يقدم كما هو (AS IS) لأغراض تعليمية. استخدام ميزة (التفعيل الكامل وحقن الذاكرة) قد يظهر كإنذار كاذب (False Positive) في برامج الحماية، لذا يُنصح باستخدام ميزة الـ Freeze كأفضل بديل آمن ومستقر مدى الحياة."
        )
        
        try:
            bot.edit_message_text(
                idm_desc, user_id, call.message.message_id, 
                reply_markup=markup, parse_mode="Markdown"
            )
        except Exception as e:
            print(f"❌ خطأ في قسم IDM: {e}")
        return

    # ===== 🌐 قسم Server 1 =====
    elif cd == "free_server1":
        try: bot.answer_callback_query(call.id)
        except: pass
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("📥 الدخول إلى السيرفر (Mega)", url="https://mega.nz/folder/JpJmnaKK#0CkdhqlqyuBPqWZqPSbTVA"),
            types.InlineKeyboardButton("🔙 رجوع للأدوات المجانية", callback_data="main_free_tools")
        )
        
        server_text = (
            "🌐 **Server 1 (ملفات وأدوات السيرفر الأول):**\n\n"
            "مرحباً بك في السيرفر الأول! يمكنك الوصول إلى كافة الملفات المرفوعة عبر الرابط المباشر أدناه بأقصى سرعة تحميل من سيرفرات ميجا.\n\n"
            "👇 **اضغط على الزر بالأسفل للدخول للرابط:**"
        )
        
        try:
            bot.edit_message_text(
                server_text, call.message.chat.id, call.message.message_id, 
                reply_markup=markup, parse_mode="Markdown"
            )
        except Exception as e:
            print(f"❌ خطأ في قسم Server 1: {e}")
        return
    # 🎯 صفحة تفاصيل عرض Max Tech Server (تفتح عند الضغط على الزر أعلاه)
    elif cd == "page_max_tech_server":
        track_tool("تفاصيل عرض ماكس تيك", user_id)
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("📱 واتساب للطلب",  url=WHATSAPP_URL),
            types.InlineKeyboardButton("👤 تيلجرام للإدارة", url=TELEGRAM_ADMIN)
        )
        markup.add(types.InlineKeyboardButton("🔙 رجوع لقسم العروض", callback_data="haitham_offers"))
        
        # 💡 يمكنك تعديل النص أدناه وكتابة مميزات وأسعار سيرفرك كما تحب
        MAX_TECH_DESC = (
            "🔥 **سيرفر Max Tech Server المتكامل:**\n\n"
            "الآن بين يديك أقوى الخدمات والحلول البرمجية الحصرية بأفضل الأسعار الممكنة في السوق.\n\n"
            "📌 **مميزات العرض الحالي:**\n"
            "• دعم فني متواصل وحلول سريعة لجميع مشاكل الهواتف.\n"
            "• تفعيل فوري وباقات مخصصة تناسب احتياجاتك التقنية.\n\n"
            "💬 للتواصل والاشتراك الفوري في العرض، اختر وسيلة التواصل المناسبة لك أدناه:"
        )
        bot.edit_message_text(MAX_TECH_DESC, user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        return

    # ===== 💾 أداة النسخ الاحتياطي Acronis =====
    elif cd == "free_acronis_backup":
        try: bot.answer_callback_query(call.id)
        except: pass
        if 'track_tool' in globals(): track_tool("أداة Acronis Backup", user_id)
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("📥 تحميل البرنامج من تيليجرام", url="https://t.me/haithamMax1/1005"),
            types.InlineKeyboardButton("🔙 رجوع لقسم الأدوات المجانية", callback_data="main_free_tools")
        )
        
        acronis_desc = (
            "💾 **نسخة احتياطية من الملفات أو النظام والويندوز بأكمله:**\n\n"
            "برنامج **Acronis True Image 2021** (والذي تغير اسمه لاحقاً إلى Acronis Cyber Protect Home Office) هو من أقوى البرامج وأشهرها في مجال النسخ الاحتياطي وإدارة الأقراص الصلبة.\n"
            "البرنامج لا يقتصر عمله على أخذ نسخة للملفات العادية فحسب، بل هو أداة متكاملة لإنقاذ النظام بالكامل.\n\n"
            "📌 **إليك أهم ما يقوم به البرنامج بالتفصيل:**\n\n"
            "1️⃣ **أخذ صورة كاملة للنظام (System Image Backup):**\n"
            "يسمح لك بأخذ \"صورة مطابقة\" للقرص الصلب بالكامل، بما في ذلك الويندوز، البرامج، والتعريفات.\n"
            "💡 *الفائدة:* إذا انهار النظام أو امتلأ بالفيروسات، يمكنك استعادته في دقائق ليعود تماماً كما كان.\n\n"
            "2️⃣ **استنساخ الأقراص (Disk Cloning):**\n"
            "نسخ القرص القديم بكامل محتوياته إلى قرص جديد (SSD/HDD) بشكل مباشر.\n"
            "💡 *الفائدة:* ممتازة عند الترقية لهارد سريع؛ حيث يعمل النظام فوراً بدون إعادة تهيئة.\n\n"
            "3️⃣ **الاستعادة على أجهزة مختلفة (Universal Restore):**\n"
            "استعادة النسخة على كمبيوتر جديد يمتلك مواصفات مختلفة، حيث يعالج توافق التعريفات ويمنع شاشة الموت الزرقاء.\n\n"
            "4️⃣ **الحماية الاستباقية (Active Protection):**\n"
            "نظام حماية مدمج بالذكاء الاصطناعي لمنع برامج الفدية (Ransomware) من تشفير ملفاتك.\n\n"
            "5️⃣ **إنشاء فلاشة إنقاذ (Rescue Media Builder):**\n"
            "حرق أداة إقلاع (Bootable) على فلاش ميموري (USB).\n"
            "💡 *الفائدة:* الإقلاع من الفلاشة واستعادة النظام حتى إذا كان الويندوز لا يفتح إطلاقاً.\n\n"
            "🎯 **الخلاصة:** كفني برمجة هواتف وكمبيوتر، هذا البرنامج يعتبر أداة أساسية في عملك لأخذ نسخ احتياطية لأنظمة العملاء ولترقية الأقراص دون تضييع الوقت.\n\n"
            "📦 **الحجم:** `447 MB`\n"
            "🔐 **كلمة السر لفك الضغط:** `@software_application`\n"
            "━━━━━━━━━━━━━━━━━\n"
            "👇 **اضغط أدناه لتحميل البرنامج:**"
        )
        
        bot.edit_message_text(
            acronis_desc, user_id, call.message.message_id, 
            reply_markup=markup, parse_mode="Markdown"
        )
        return

    # ====================================================================
    # 🔥 1. قسم عروض هيثم ماكس المطور (القائمة الرئيسية)
    # ====================================================================
    if cd == "haitham_offers":
        try: bot.answer_callback_query(call.id)
        except: pass
        if 'track_tool' in globals(): track_tool("دخول قسم العروض", user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🔥 عرض Max Tech Server الحصري", callback_data="page_max_tech_server"),
            types.InlineKeyboardButton("🤖 عروض ChatGPT Plus (4 عروض)", callback_data="h_sub_gpt"),
            types.InlineKeyboardButton("🍿 عروض نتفلكس (Netflix)", callback_data="h_sub_netflix"),
            types.InlineKeyboardButton("🎬 عروض Capcut Pro (4 عروض)", callback_data="h_sub_capcut"),
            types.InlineKeyboardButton("🎨 Canva Pro 1 Year - $8", callback_data="h_prod_canva_1y"),
            types.InlineKeyboardButton("▶️ عروض يوتيوب بريميوم (2 عرض)", callback_data="h_sub_yt"),
            types.InlineKeyboardButton("🖱️ عروض API Cursor Pro (3 عروض)", callback_data="h_sub_cursor"),
            types.InlineKeyboardButton("✨ أدوات الذكاء الاصطناعي والتصميم", callback_data="h_sub_ai"),
            types.InlineKeyboardButton("⚡ عروض Grok Super (4 عروض)", callback_data="h_sub_grok"),
            types.InlineKeyboardButton("🎵 عروض الصوتيات والفيديو", callback_data="h_sub_media"),
            types.InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="back_start")
        )
        bot.edit_message_text(
            "⚡ **عروض هيثم ماكس الحصرية:**\n\nمرحباً بك في قسم العروض الضخم، اختر الفئة أو الخدمة المطلوبة أدناه لاستعراض التفاصيل:", 
            user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown"
        )
        return

    # --- تفريعات عروض CHAT GPT ---
    elif cd == 'h_sub_gpt':
        try: bot.answer_callback_query(call.id)
        except: pass
        markup = types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton('CHAT GPT PLUS 1 Month ($9.91)', callback_data='h_prod_gpt_plus_1m'),
            types.InlineKeyboardButton('ChatGPT Plus Level 30D ($9.91)', callback_data='h_prod_gpt_plus_level_30d'),
            types.InlineKeyboardButton('ChatGPT Plus Apple Pay 30D ($9.91)', callback_data='h_prod_gpt_plus_apple_pay_30d'),
            types.InlineKeyboardButton('ChatGPT Plus ApplePay 1M ($8.77)', callback_data='h_prod_gpt_plus_apple_pay_1m_1d'),
            types.InlineKeyboardButton('🔙 رجوع للعروض', callback_data='haitham_offers')
        )
        bot.edit_message_text("🤖 **عروض واشتراكات CHAT GPT:**", user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        return

    # --- تفريعات عروض نتفلكس ---
    elif cd == 'h_sub_netflix':
        try: bot.answer_callback_query(call.id)
        except: pass
        markup = types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton('Netflix Premium 4K - 1 Month ($3.50)', callback_data='h_prod_netflix_1m'),
            types.InlineKeyboardButton('🔙 رجوع للعروض', callback_data='haitham_offers')
        )
        bot.edit_message_text("🍿 **عروض اشتراكات نتفلكس (Netflix):**", user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        return

    # --- تفريعات كاب كات برو ---
    elif cd == 'h_sub_capcut':
        try: bot.answer_callback_query(call.id)
        except: pass
        markup = types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton('Capcut Pro 1 Month', callback_data='h_prod_capcut_1m'),
            types.InlineKeyboardButton('Capcut Pro 3 Months', callback_data='h_prod_capcut_3m'),
            types.InlineKeyboardButton('Capcut Pro 6 Months', callback_data='h_prod_capcut_6m'),
            types.InlineKeyboardButton('Capcut Pro 1 Year', callback_data='h_prod_capcut_1y'),
            types.InlineKeyboardButton('🔙 رجوع للعروض', callback_data='haitham_offers')
        )
        bot.edit_message_text("🎬 **عروض كاب كات برو:**", user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        return

    # --- تفريعات يوتيوب بريميوم ---
    elif cd == 'h_sub_yt':
        try: bot.answer_callback_query(call.id)
        except: pass
        markup = types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton('YouTube Premium 6M - $11', callback_data='h_prod_yt_6m'),
            types.InlineKeyboardButton('YouTube Premium 12M - $25', callback_data='h_prod_yt_12m'),
            types.InlineKeyboardButton('🔙 رجوع للعروض', callback_data='haitham_offers')
        )
        bot.edit_message_text("▶️ **عروض يوتيوب بريميوم:**", user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        return

    # --- تفريعات Cursor Pro ---
    elif cd == 'h_sub_cursor':
        try: bot.answer_callback_query(call.id)
        except: pass
        markup = types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton('API Cursor Pro 200/day - $18', callback_data='h_prod_cursor_200'),
            types.InlineKeyboardButton('API Cursor Pro 2600 - $15', callback_data='h_prod_cursor_2600'),
            types.InlineKeyboardButton('API Cursor Pro 6500 - $18', callback_data='h_prod_cursor_6500'),
            types.InlineKeyboardButton('🔙 رجوع للعروض', callback_data='haitham_offers')
        )
        bot.edit_message_text("🖱️ **عروض API Cursor Pro:**", user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        return

    # --- تفريعات الذكاء الاصطناعي ---
    elif cd == 'h_sub_ai':
        try: bot.answer_callback_query(call.id)
        except: pass
        markup = types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton('Lovable AI PRO 1M - $20', callback_data='h_prod_lovable_1m'),
            types.InlineKeyboardButton('Loveable Pro Lite 1Y - $10', callback_data='h_prod_lovable_lite'),
            types.InlineKeyboardButton('Figma Pro Education 1Y - $11', callback_data='h_prod_figma_edu'),
            types.InlineKeyboardButton('Leonardo AI 8.5K - $5', callback_data='h_prod_leonardo_ai'),
            types.InlineKeyboardButton('🔙 رجوع للعروض', callback_data='haitham_offers')
        )
        bot.edit_message_text("✨ **أدوات الذكاء الاصطناعي والتصميم:**", user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        return

    # --- تفريعات Grok Super ---
    elif cd == 'h_sub_grok':
        try: bot.answer_callback_query(call.id)
        except: pass
        markup = types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton('Grok Super 1 Month - $18', callback_data='h_prod_grok_1m'),
            types.InlineKeyboardButton('Grok Super 3 Months - $26', callback_data='h_prod_grok_3m'),
            types.InlineKeyboardButton('Grok Super 6 Months - $40', callback_data='h_prod_grok_6m'),
            types.InlineKeyboardButton('Grok Super 12 Months - $75', callback_data='h_prod_grok_12m'),
            types.InlineKeyboardButton('🔙 رجوع للعروض', callback_data='haitham_offers')
        )
        bot.edit_message_text("⚡ **عروض Grok Super:**", user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        return

    # --- تفريعات الصوتيات والفيديو ---
    elif cd == 'h_sub_media':
        try: bot.answer_callback_query(call.id)
        except: pass
        markup = types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton('SUNO PRO 1 Month - $12', callback_data='h_prod_suno_pro'),
            types.InlineKeyboardButton('Elevenlabs Creator 131K - $12', callback_data='h_prod_elevenlabs'),
            types.InlineKeyboardButton('Kling Ultra 27.5K 1M - $85', callback_data='h_prod_kling_ultra'),
            types.InlineKeyboardButton('🔙 رجوع للعروض', callback_data='haitham_offers')
        )
        bot.edit_message_text("🎵 **عروض الصوتيات والفيديو:**", user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        return

    # --- معالج عرض تفاصيل أي منتج تلقائياً ---
    elif cd.startswith('h_prod_'):
        try: bot.answer_callback_query(call.id)
        except: pass
        prod_key = cd.replace('h_prod_', '')
        if prod_key in all_hitham_products:
            desc = hmaxi18n.translate_product_description(
                prod_key, all_hitham_products[prod_key], hmaxi18n.get_language(user_id)
            )
            markup = types.InlineKeyboardMarkup(row_width=1).add(
                types.InlineKeyboardButton('🛒 طلب الخدمة الآن', callback_data='h_order_now'),
                types.InlineKeyboardButton('🔙 رجوع للقائمة', callback_data='haitham_offers')
            )
            bot.edit_message_text(desc, user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        return

    # --- معالج زر طلب الخدمة (التواصل) ---
    elif cd == 'h_order_now':
        try: bot.answer_callback_query(call.id)
        except: pass
        text = (
            "🛒 **لإتمام الطلب وشراء الخدمة:**\n\n"
            "تواصل معنا مباشرة عبر الروابط التالية لإتمام الدفع واستلام طلبك فوراً 🚀\n\n"
            f"• تليجرام: {TELEGRAM_ADMIN}\n"
            f"• واتساب: {WHATSAPP_URL}"
        )
        markup = types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton('💬 تواصل عبر واتساب', url=WHATSAPP_URL),
            types.InlineKeyboardButton('✈️ تواصل عبر تيليجرام', url=TELEGRAM_ADMIN),
            types.InlineKeyboardButton('🔙 رجوع للعروض', callback_data='haitham_offers')
        )
        bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        return

    
    # ====================================================================
    # 🔥 2. قسم العروض المدفوعة (الأساسية)
    # ====================================================================
    elif cd == "main_paid_offers":
        try: bot.answer_callback_query(call.id)
        except: pass
        markup = types.InlineKeyboardMarkup(row_width=1).add(
            types.InlineKeyboardButton("💎 عرض جمناي برو + 5 تيرا", callback_data="gemini_5tb_offer"),
            types.InlineKeyboardButton("🛑 حسابات آيكلاود جاهزة", callback_data="paid_icloud_accounts"),
            types.InlineKeyboardButton("📦 سيرفرات وتفعيل بوكسات", callback_data="contact_paid_service"),
            types.InlineKeyboardButton("🔑 حسابات دنقل مدفوعة", callback_data="contact_paid_service"),
            types.InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="back_start")
        )
        bot.edit_message_text(
            "🔥 **قسم العروض المدفوعة الحصرية:**\n\n"
            "مرحباً بك في قسم الخدمات المدفوعة الشاملة. نوفر لك تفعيل الحسابات والبوكسات بأفضل الأسعار وبسرعة فائقة.\n\n"
            "💡 اختر الخدمة المطلوبة أو تواصل مع الإدارة مباشرة عبر الأزرار أدناه:", 
            user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown"
        )
        return

    elif cd == "gemini_5tb_offer":
        try: bot.answer_callback_query(call.id)
        except: pass
        if 'track_tool' in globals(): track_tool("عرض جمناي برو + 5 تيرا", user_id)
        markup = types.InlineKeyboardMarkup(row_width=2).add(
            types.InlineKeyboardButton("📱 واتساب", url=WHATSAPP_URL),
            types.InlineKeyboardButton("👤 تيلجرام", url=TELEGRAM_ADMIN)
        ).add(types.InlineKeyboardButton("🔙 رجوع للعروض", callback_data="main_paid_offers"))
        
        display_text = (
            "🚀 **عرض الذكاء الاصطناعي الأقوى:**\n\n"
            "• اشتراك Gemini Pro (جمناي برو).\n"
            "• مساحة تخزين إضافية ضخمة بحجم 5 تيرا بايت.\n"
            "• 🗓️ المدة: 18 شهراً كاملاً!\n"
            "💸 السعر: **10 دولار فقط!**\n\n\n"
            "🎁 هذا العرض إهداء من: **هيثم ماكس** 🎁\n\n"
            "━━━━━━━━━━━━━━━━━\n"
            "🛒 لطلب الاشتراك وتفعيل العرض فوراً، اضغط على أحد أزرار التواصل أدناه:"
        )
        bot.edit_message_text(display_text, user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        return

    elif cd == "paid_icloud_accounts":
        try: bot.answer_callback_query(call.id)
        except: pass
        if 'track_tool' in globals(): track_tool("مشاهدة حسابات آيكلاود جاهزة", user_id)
        markup = types.InlineKeyboardMarkup(row_width=2).add(
            types.InlineKeyboardButton("📱 واتساب", url=WHATSAPP_URL),
            types.InlineKeyboardButton("👤 تيلجرام", url=TELEGRAM_ADMIN)
        ).add(types.InlineKeyboardButton("🔙 رجوع للعروض", callback_data="main_paid_offers"))
        
        display_text = (
            "🛑 **حسابات آيكلاود جاهزة ومضمونة:**\n\n"
            "🍏 **Apple ID - iCloud Account**\n\n"
            "إذا واجهتك مشكلة عند محاولة إنشاء حساب جديد، بإمكانك الآن شراء حساب آيكلاود جاهز ومضمون 100% بنقرة زر واحدة.\n\n"
            "📌 **مميزات وتفاصيل الحسابات:**\n"
            "• **مُفعّل بالكامل:** جاهز للاستخدام مباشرة على متجر التطبيقات الأمريكي (App Store).\n"
            "• **رسمي وآمن:** يعمل بكفاءة عالية على الآيكلاود والمتجر معاً بدون أي مشاكل تعليق ✅.\n"
            "• **الملكية الكاملة:** سيتم إضافة رقمك أو رقم زبونك مباشرةً ثم إزالة رقم المحل نهائياً 🗝️.\n\n"
            "💵 **الأسعار:**\n"
            "• بسعر **3$ USDT** عالمياً.\n"
            "• أو بسعر **20 دينار** داخل دولة ليبيا 🇱🇾.\n"
            "━━━━━━━━━━━━━━━━━\n"
            "📥 للشراء الفوري، يرجى الضغط على أحد أزرار التواصل بالأسفل:"
        )
        bot.edit_message_text(display_text, user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        return

    elif cd == "contact_paid_service":
        try: bot.answer_callback_query(call.id)
        except: pass
        markup = types.InlineKeyboardMarkup(row_width=2).add(
            types.InlineKeyboardButton("📱 واتساب", url=WHATSAPP_URL),
            types.InlineKeyboardButton("👤 تيلجرام", url=TELEGRAM_ADMIN)
        ).add(types.InlineKeyboardButton("🔙 رجوع للعروض", callback_data="main_paid_offers"))
        
        bot.edit_message_text(
            "💳 **لطلب الخدمة أو التفعيل الفوري:**\n\nيرجى التواصل مع الإدارة مباشرة لتزويدنا بالبيانات عبر وسائل الدعم المتاحة:", 
            user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown"
        )
        return


    # ===== عروض الذكاء الاصطناعي =====
    elif cd == "main_ai_offers":
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("💎 GEMINI", callback_data="ai_cat_gemini"),
            types.InlineKeyboardButton("🤖 GPT",    callback_data="ai_cat_gpt"),
        )
        markup.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="back_start"))
        bot.edit_message_text(
            "🤖 **عروض الذكاء الاصطناعي:**",
            user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown"
        )

    elif cd == "ai_cat_gemini":
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("💎 GEMINI PRO 12 شهر", callback_data="page_ai_gemini_12"),
            types.InlineKeyboardButton("💎 GEMINI PRO 18 شهر", callback_data="page_ai_gemini_18"),
            types.InlineKeyboardButton("🔙 رجوع",              callback_data="main_ai_offers"),
        )
        bot.edit_message_text(
            "💎 **عروض GEMINI PRO:**",
            user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown"
        )

    elif cd == "ai_cat_gpt":
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🤖 GPT PLUS شهر", callback_data="page_ai_gpt_plus"),
            types.InlineKeyboardButton("🤖 GPT GO سنة",   callback_data="page_ai_gpt_go"),
            types.InlineKeyboardButton("🔙 رجوع",         callback_data="main_ai_offers"),
        )
        bot.edit_message_text(
            "🤖 **عروض GPT:**",
            user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown"
        )

    elif cd.startswith("page_ai_"):
        key = cd.replace("page_ai_", "")
        if key in DATA["ai_offers"]:
            offer_name = DATA["ai_offers"][key][0]
            track_tool(offer_name, user_id)
            back_call = "ai_cat_gemini" if "gemini" in key else "ai_cat_gpt"
            markup = types.InlineKeyboardMarkup(row_width=2)
            markup.add(
                types.InlineKeyboardButton("📱 واتساب", url=WHATSAPP_URL),
                types.InlineKeyboardButton("👤 تيلجرام", url=TELEGRAM_ADMIN),
            )
            markup.add(types.InlineKeyboardButton("🔙 رجوع", callback_data=back_call))
            bot.edit_message_text(
                f"✨ **العرض:** {offer_name}\n\n📞 للاشتراك تواصل معنا عبر الأزرار أدناه:",
                user_id, call.message.message_id,
                reply_markup=markup, parse_mode="Markdown"
            )

    # ===== نظام النقاط =====
    elif cd == "points_sys":
        try:
            bot.delete_message(user_id, call.message.message_id)
        except:
            pass
        show_my_profile(user_id)

    # ===== طلب أداة =====
    elif cd == "req_tool":
        log_interaction(user_id, "طلب أداة")
        bot.send_message(user_id, "📝 أرسل اسم الأداة التي تريدها:")
        bot.register_next_step_handler(call.message, handle_user_request, "طلب أداة خاصة")

    # ===== طلب حلب تك =====
# ================= 🆕 نظام حلب تك (HalabTech) المطور والمصلح بالكامل (محدث بالخانات المجانية) =================
    elif cd == "halabtech_req":
        bot.answer_callback_query(call.id)
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("📱 فلاشات ورومات رسمية", callback_data="halab_cat_firmware"),
            types.InlineKeyboardButton("🔤 قسم تعريب أنظمة", callback_data="halabtech_arabization"),
        )
        markup.add(
            types.InlineKeyboardButton("🔓 تخطي وحمايات FRP & Dump", callback_data="halab_cat_security"),
            types.InlineKeyboardButton("📐 طلب ملف حلب تك 💰", callback_data="halab_request_file"),
        )
        markup.row(types.InlineKeyboardButton("🎁 ملفات مجانية حلب تك", callback_data="halabtech_free_files"))
        markup.row(types.InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data="back_start"))
        
        text = (
            "🛠️ **سيرفر ملفات حلب تك (HalabTech) الشامل:**\n\n"
            "مرحباً بك في لوحة سحب ملفات حلب تك المدفوعة والمميزة.\n\n"
            "💡 **اختر القسم البرمجي الذي تبحث عن ملفات بداخله أو اطلب ملفك المباشر:**"
        )
        bot.edit_message_text(text, user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        return

    # 🎁 معالج صفحة ملفات حلب تك المجانية (تم تزويده بالزر الجديد بنجاح)
    elif cd == "halabtech_free_files":
        bot.answer_callback_query(call.id)
        track_tool("قسم ملفات حلب تك المجانية", user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🔓 حل مشكلة حظر الواتس بشكل نهائي", callback_data="halab_free_whatsapp"),
            types.InlineKeyboardButton("📱 حذف حساب Mi Account لجهاز Redmi Note 12 Pro 4G", callback_data="halab_free_redmi_mi"), # 🌟 الزر الجديد
            types.InlineKeyboardButton("🔙 رجوع لقسم حلب تك الرئيسي", callback_data="halabtech_req")
        )
        display_text = (
            "🎁 **قسم ملفات حلب تك الحرة والمجانية:**\n\n"
            "مرحباً بك في القسم المجاني المخصص لأقوى الحلول، السكريبتات، والملفات المفتوحة المقتبسة مجاناً لجميع مهندسي البرمجة.\n\n"
            "💡 **اختر الحل التقني المطلوب أدناه لعرض الشرح الكامل وروابط التحميل السريعة:**"
        )
        bot.edit_message_text(display_text, user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        return

    # 📱 معالج عرض ثغرة وشرح تخطي حساب شاومي Redmi Note 12 Pro 4G (حصري ومضمون)
    elif cd == "halab_free_redmi_mi":
        bot.answer_callback_query(call.id)
        track_tool("تخطي حساب مي نوت 12 برو 4 جي", user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🔗 رابط المقال والملف الأصلي (HalabTech)", url="https://halabtech.com/redmi-note-12-pro-4g-mi-account-remove-halabtech/"),
            types.InlineKeyboardButton("🔙 رجوع للملفات المجانية", callback_data="halabtech_free_files")
        )
        
        display_text = (
            "📱 **حذف وتخطي حساب Mi Account لجهاز Redmi Note 12 Pro 4G:**\n"
            "🔥 الحل النهائي لفك وإزالة حساب شاومي نهائياً ومنع إعادة الإغلاق الذكي بعد تشغيل شبكة الـ Wi-Fi.\n\n"
            "📦 **معلومات الهاتف المستهدف (Target Device):**\n"
            "• **الموديل:** Redmi Note 12 Pro 4G\n"
            "• **اسم الحماية المخصص:** `sweet_k6a`\n"
            "• **نوع المعالج:** Qualcomm Snapdragon\n\n"
            "📝 **خطوات العمل والإنهاء البرمجي بالملي:**\n"
            "1️⃣ قم بتحميل ملف التخطي المخصص المفكوك عبر الرابط أدناه وضعه على الكمبيوتر.\n"
            "2️⃣ يجب فك الظهر الخلفي للهاتف وتوصيل نقطتي الفحص **(Test Point)** لإدخال الهاتف بوضعية الـ **EDL Mode**.\n"
            "3️⃣ تأكد من ظهور تعريف الهاتف على إدارة الأجهزة بالكمبيوتر باسم:\n"
            "👈 `Qualcomm HS-USB QDLoader 9008`.\n"
            "4️⃣ افتح أداة التفليش المتاحة لديك (مثل Mi Flash أو أي أداة مجانية تدعم سحب ملفات حلب تك).\n"
            "5️⃣ قم باختيار مجلد الفك والملفات المخصصة، ثم اضغط على **Flash**.\n"
            "6️⃣ انتظر حتى يكتمل شريط التحميل وظهور كلمة **Success** بنجاح.\n\n"
            "🔄 الآن قم بإعادة تركيب البطارية وتشغيل الهاتف وتخطي الإعدادات الأولية.. ومبارك عليك إزالة حساب شاومي نهائياً وثبات استقرار النظام مجاناً وبدون أي مشاكل!"
        )
        bot.edit_message_text(display_text, user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        return

    # 🔓 معالج عرض ثغرة وشرح حل حظر الواتساب نهائياً 
    elif cd == "halab_free_whatsapp":
        bot.answer_callback_query(call.id)
        track_tool("حل مشكلة حظر الواتس حلب تك", user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🔗 رابط الملف الأصلي (HalabTech)", url="https://halabtech.com/%D8%AD%D9%84-%D9%85%D8%B4%D9%83%D9%84%D8%A9-%D8%AD%D8%B8%D8%B1-%D8%A7%D9%84%D9%88%D8%A7%D8%AA%D8%B3-%D8%A8%D8%B4%D9%83%D9%84-%D9%86%D9%87%D8%A7%D8%A6%D9%8A-%D9%85%D8%B9-%D8%A7%D9%85%D9%83%D8%A7%D9%86/"),
            types.InlineKeyboardButton("📥 تنزيل الملف المباشر (Drive)", url="https://drive.google.com/drive/folders/1Us0oc59pxqbuB5iKSci7hAEuA19PR6SZ"),
            types.InlineKeyboardButton("🔙 رجوع للملفات المجانية", callback_data="halabtech_free_files")
        )
        
        display_text = (
            "🔓 **حل مشكلة حظر الواتس بشكل نهائي:**\n"
            "🔥 حل قطعي مع إمكانية حذف وإعادة تثبيت التطبيق بدون نقل وبدون هاتف آخر تماماً!\n\n"
            "⚙️ **المتطلبات الأساسية:** صلاحية الـ **Root** مفعّلة بجهازك.\n\n"
            "📝 **طريقة العمل والخطوات المضمونة بالتفصيل:**\n"
            "1️⃣ نفتح السكريبت الآتي المرفق بالتحميل ونختار **رقم 1**.\n"
            "2️⃣ قم بإعطاء إذن تصحيح الـ **USB** للكمبيوتر، وانتظر حتى تنتهي العملية بالكامل.\n"
            "3️⃣ بعدها نتوجه مباشرة إلى تطبيق **Magisk** 👈 ثم نفتح قسم **الإضافات**.\n"
            "4️⃣ **أولاً:** نضغط على خيار **تحديث** (⚠️ *تنبيه هام: لا تعيد تشغيل الهاتف بعد الانتهاء*).\n"
            "5️⃣ ثم نضغط **تشغيل**.\n"
            "6️⃣ **ثانياً:** نضغط على **تشغيل** واختيار كافّة التطبيقات بداخل الواجهة.\n"
            "7️⃣ **ثالثاً:** نضغط على **تشغيل** واختيار تطبيق **الواتساب** فقط.\n\n"
            "🔄 بعد الانتهاء تماماً، قم بعمل **إعادة تشغيل (Reboot)** للهاتف.. ومبارك عليك حل المشكلة بشكل نهائي بدون نقل وبدون هاتف آخر!\n\n"
            "👤 **بواسطة المهندس والمبدع:** خالد الجاسم"
        )
        bot.edit_message_text(display_text, user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        return

    # 📐 معالج صفحة تفاصيل طلب ملف حلب تك المدفوع 3 دولار
    elif cd == "halab_request_file":
        bot.answer_callback_query(call.id)
        track_tool("صفحة طلب ملف حلب تك 3 دولار", user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("💸 3 دولار", callback_data="halab_paid_contact"),
            types.InlineKeyboardButton("🔙 رجوع لقسم حلب تك", callback_data="halabtech_req")
        )
        display_text = (
            "📐 **طلب سحب أي ملف من موقع حلب تك:**\n\n"
            "أهلاً وسهلاً بك، يمكننا بإذن الله سحبه ورفعه لك عبر البريد، أي ملف تريده من موقع حلب تك.\n\n"
            "💰 **سعر الخدمة:** 3 دولار فقط (ما يعادل 1600 ريال يمني قديم / 11 ريال سعودي).\n\n"
            "📞 للطلب يرجى التواصل بنا عبر النقر على زر السيرفر أدناه:"
        )
        bot.edit_message_text(display_text, user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        return

    # 📞 معالج كشف معلومات التواصل عند الضغط على زر 3 دولار
    elif cd == "halab_paid_contact":
        bot.answer_callback_query(call.id)
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("📱 تواصل عبر واتساب", url=WHATSAPP_URL),
            types.InlineKeyboardButton("👤 تواصل عبر تليجرام", url=TELEGRAM_ADMIN)
        )
        markup.add(types.InlineKeyboardButton("🔙 رجوع لصفحة الطلب", callback_data="halab_request_file"))
        
        contact_text = (
            "📞 **معلومات التواصل لطلب ملف حلب تك المدفوع:**\n\n"
            "أهلاً بك يا غالي! لإرسال رابط الملف وإتمام عملية الدفع والتنفيذ الفوري، يرجى التواصل معنا عبر حسابات الإدارة الرسمية التالية:\n\n"
            "🟢 **رقم الواتساب الإداري:** `+967 772 773 388`\n"
            "🔵 **معرف التيلجرام المباشر:** @hithamMax\n\n"
            "📥 اضغط على أحد الأزرار بالأسفل لفتح محادثة فورية معنا مباشرة:"
        )
        bot.edit_message_text(contact_text, user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        return

    # معالج الأقسام الداخلية الثلاثة المتبقية لحلب تك المدفوع
    elif cd.startswith("halab_cat_"):
        cat_type = cd.replace("halab_cat_", "")
        cat_names = {
            "firmware": "فلاشات ورومات رسمية",
            "network": "ملفات شبكة وسيريال CERT/EFS",
            "security": "تخطي وحمايات FRP & Dump"
        }
        name = cat_names.get(cat_type, "ملفات حلب تك")
        track_tool(f"قسم حلب تك - {name}", user_id)
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton(f"📥 اضغط هنا لطلب ملف من قسم ({name})", callback_data=f"halab_submit_{cat_type}"),
            types.InlineKeyboardButton("🔙 رجوع لقسم حلب تك الرئيسي", callback_data="halabtech_req")
        )
        
        display_text = (
            f"🛠️ **بوابة حلب تك الحصرية 👈 قسم: {name}**\n\n"
            f"نوفر لك إمكانية سحب وتحميل أي ملف مدفوع من موقع حلب تك بداخل تصنيف **{name}** فوراً وبأعلى سرعة سيرفر.\n\n"
            "📌 **خطوات الحصول على الملف:**\n"
            "1. اذهب لموقع حلب تك الرسمي وابحث عن الملف المخصص لجهازك.\n"
            "2. قم بنسخ رابط الملف أو اسمه الكامل بدقة.\n"
            "3. اضغط على زر طلب الملف بالأسفل للتواصل معنا وإرسال الرابط.\n"
            "━━━━━━━━━━━━━━━━━\n"
            "📥 لطلب ملفك الآن, اضغط أدناه:"
        )
        bot.edit_message_text(display_text, user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        return
        
    # عرض قائمة ملفات التعريب ديناميكياً
    elif cd == "halabtech_arabization":
        markup = types.InlineKeyboardMarkup(row_width=1)
        
        arab_data = DATA.get("halabtech_arabization", {
            "t387v":  ("📱 SM-T387V U3 (Arabic)", "https://support.halabtech.com/index.php?a=downloads&b=file&id=104983", "https://www.mediafire.com/file/cfqitvgt28yi089/Setup_New_Translation_Language_HalabTech.rar/file"),
            "t377r4": ("📱 T377R4 7.0 Arabic Turkey 1 Min", "https://support.halabtech.com/index.php?a=downloads&b=file&id=104983", "https://drive.google.com/file/d/1Ws6OmwXHWFtwyE2r2iRYos2hLp2SqDjN/view"),
        })
        
        btns = [
            types.InlineKeyboardButton(v[0], callback_data=f"link_arab_{k}")
            for k, v in arab_data.items()
        ]
        markup.add(*btns)
        markup.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="halabtech_req"))
        
        bot.edit_message_text("🔤 **قسم تعريب الأنظمة الحصري:**\n\nاختر ملف التعريب المطلوب لعرض روابط الدعم والتحميل المتاحة:", user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        return

    # معالج فتح صفحة التحميل الثنائية وعرض الباسورد ذكياً لملفات التعريب
    elif cd.startswith("link_arab_"):
        key = cd.replace("link_arab_", "")
        arab_data = DATA.get("halabtech_arabization", {})
        
        if key in arab_data:
            tool_name, support_link, system_link = arab_data[key]
            track_tool(tool_name, user_id)
            
            pass_text = ""
            if key == "t377r4":
                pass_text = "\n\n🔑 **كلمة سر فك الضغط (Pass):** `HOSAM`\n*(اضغط على الباسورد لنسخه تلقائياً)*"
                
            display_text = f"🔤 **ملف تعريب: {tool_name}**\n\nجاهز الآن! يحتوي هذا القسم على رابط الدعم ورابط التحميل المباشر. اختر ما تريده أدناه:{pass_text}"
            
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(
                types.InlineKeyboardButton("🔗 رابط الدعم والمصدر (HalabTech)", url=support_link),
                types.InlineKeyboardButton("📥 تحميل ملف النظام المباشر", url=system_link)
            )
            markup.add(types.InlineKeyboardButton("🔙 رجوع للقائمة", callback_data="halabtech_arabization"))
            
            bot.edit_message_text(display_text, user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        else:
            bot.answer_callback_query(call.id, "❌ لم يتم العثور على ملف التعريب.")
        return

    # عرض أزرار التواصل المباشر عند السحب للملفات المدفوعة
    elif cd.startswith("halab_submit_"):
        cat_type = cd.replace("halab_submit_", "")
        cat_names = {
            "firmware": "فلاشات ورومات رسمية",
            "network": "ملفات شبكة وسيريال CERT/EFS",
            "security": "تخطي وحمايات FRP & Dump"
        }
        name = cat_names.get(cat_type, "ملفات حلب تك")
        log_interaction(user_id, f"طلب تواصل: {name}")
        
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("📱 تواصل عبر واتساب", url=WHATSAPP_URL),
            types.InlineKeyboardButton("👤 تواصل عبر تليجرام", url=TELEGRAM_ADMIN)
        )
        markup.add(
            types.InlineKeyboardButton("🔙 رجوع للقسم", callback_data=f"halab_cat_{cat_type}")
        )
        
        contact_text = (
            f"📞 **قسم طلب ملفات حلب تك المدفوعة 👈 ({name}):**\n\n"
            "أهلاً بك يا غالي! لسحب هذا الملف فوراً وتزويدك برابط التحميل المباشر، يرجى نسخ رابط الملف من موقع حلب تك وإرساله لنا مباشرة عبر أرقام وحسابات التواصل الرسمية التالية:\n\n"
            "🟢 **رقم الواتساب الإداري:** `+967 772 773 388`\n"
            "🔵 **معرف التيلجرام المباشر:** @hithamMax\n\n"
            "━━━━━━━━━━━━━━━━━\n"
            "📥 اضغط على أحد أزرار الدعم بالأسفل لفتح المحادثة الفورية معنا:"
        )
        bot.edit_message_text(contact_text, user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        return

    
        # ===== الأنظمة النادرة =====
    elif cd == "rare_systems_main":
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("🆓 أنظمة مجانية", callback_data="rare_free_list"),
        )
        markup.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="back_start"))
        bot.edit_message_text(
            "📂 **قسم الأنظمة النادرة:**\nاختر نوع الأنظمة:",
            user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown"
        )

    elif cd == "rare_free_list":
        try: bot.answer_callback_query(call.id)
        except: pass
        
        type_str = "مجانية"
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("📱 LT", callback_data=f"rare_brand_{type_str}_LT"),
            types.InlineKeyboardButton("📱 Redmi", callback_data=f"rare_brand_{type_str}_Redmi")
        )
        markup.add(
            types.InlineKeyboardButton("📱 Samsung", callback_data=f"rare_brand_{type_str}_Samsung"),
            types.InlineKeyboardButton("📱 Vivo", callback_data=f"rare_brand_{type_str}_vivo")
        )
        markup.add(
            types.InlineKeyboardButton("📱 ZTE", callback_data=f"rare_brand_{type_str}_ZTE"),
            types.InlineKeyboardButton("📱 أخرى", callback_data=f"rare_brand_{type_str}_Other")
        )
        markup.add(types.InlineKeyboardButton("🔙 رجوع لقسم الأنظمة", callback_data="rare_systems_main"))
        
        bot.edit_message_text(
            f"📂 **أنظمة {type_str} نادرة:**\nاختر الشركة المصنعة:",
            user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown"
        )
        return

    
    # ===== قسم رومات شاومي/ريدمي (أنظمة مجانية نادرة) =====
    elif cd == "rare_brand_مجانية_Redmi":
        try: bot.answer_callback_query(call.id)
        except: pass
        if 'track_tool' in globals(): track_tool("رومات هندسة شاومي 17", user_id)
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("📥 XIAOMI 17 (pudding)", url="https://drive.google.com/file/d/1IPob5GWwj0ZbRTJWUFuvutNOcnTDMYRb/view"),
            types.InlineKeyboardButton("📥 XIAOMI 17 ULTRA (nezha)", url="https://drive.google.com/file/d/1lyczuEFxUiGYPhKX9nQ-zbWWJQriBrm8/view"),
            types.InlineKeyboardButton("📥 XIAOMI 17 PRO (pandora)", url="https://drive.google.com/file/d/17d1lMWHJbQM67HVaQCf4T8pwBDBUILzx/view"),
            types.InlineKeyboardButton("📥 XIAOMI 17 MAX (byron)", url="https://drive.google.com/file/d/1KNx5IMB1YyZib3Ts_fxOY8CQfJkd2pzH/view"),
            types.InlineKeyboardButton("📥 XIAOMI 17 PRO MAX (popsicle)", url="https://drive.google.com/file/d/16t7Q3AQ4Ct32ZzCfplfrMS1Kx6k5ZWrb/view"),
            types.InlineKeyboardButton("📥 XIAOMI 17T (chagall)", url="https://drive.google.com/file/d/1Y1MQQlx2hpxqLbzJPBA0oTQg_KLKiXQW/view"),
            types.InlineKeyboardButton("📥 XIAOMI 17T PRO (warhol)", url="https://drive.google.com/file/d/19ovGFABzIDFU_Ql6hLw49foJoMfKGN3P/view"),
            types.InlineKeyboardButton("📱 REDMI 12C", callback_data="rare_redmi_12c"),
            types.InlineKeyboardButton("🔙 رجوع لشركات الأنظمة المجانية", callback_data="rare_free_list") 
        )
        
        display_text = (
            "📱 **رومات الهندسة النادرة لسلسلة شاومي (ENG ROM KEEPNV):**\n\n"
            "هذه الرومات (Engineering ROMs) تُستخدم لأغراض الصيانة المتقدمة، الفحص الشامل، وإصلاح المشاكل العميقة في هواتف Xiaomi / Redmi الحديثة.\n\n"
            "🔐 **كلمة السر لفك الضغط لجميع الملفات:**\n"
            "`masoodmobilesoftware`\n"
            "*(اضغط على الكلمة لنسخها تلقائياً)*\n\n"
            "━━━━━━━━━━━━━━━━━\n"
            "👇 **اختر الموديل المطلوب للتحميل المباشر من Google Drive:**"
        )
        
        bot.edit_message_text(
            display_text, user_id, call.message.message_id, 
            reply_markup=markup, parse_mode="Markdown"
        )
        return

    # ===== قسم أنظمة LT المجانية وتفريعاتها =====
    elif cd == "rare_brand_مجانية_LT":
        try: bot.answer_callback_query(call.id)
        except: pass
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🔥 [حصرياً] الفلاشة الرسمية لـ LT M50 PLUS (K80)", callback_data="page_rare_lt_m50_plus"),
            types.InlineKeyboardButton("📁 مجموعة 1", callback_data="page_rare_lt_free_1"),
            types.InlineKeyboardButton("📁 مجموعة 2", callback_data="page_rare_lt_free_2"),
            types.InlineKeyboardButton("🔙 رجوع", callback_data="rare_free_list")
        )
        bot.edit_message_text(
            "📂 **أنظمة LT المجانية:**\nاختر الفلاشة أو المجموعة:",
            user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown"
        )
        return

    # 🌟 معالج صفحة الفلاشة الحصرية LT M50 PLUS
    elif cd == "page_rare_lt_m50_plus":
        try: bot.answer_callback_query(call.id)
        except: pass
        if 'track_tool' in globals(): track_tool("الفلاشة الرسمية LT M50 PLUS", user_id)
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("📥 رابط التحميل المباشر (Google Drive)", url="https://drive.google.com/file/d/1M7k9KXbJ-_JHZ3CcTPKAAmkV9UchwW3r/view"),
            types.InlineKeyboardButton("🔙 رجوع لقائمة LT", callback_data="rare_brand_مجانية_LT")
        )
        
        display_text = (
            "🔥 **[حصرياً] الفلاشة الرسمية لـ LT M50 PLUS (K80) - نظام خام رسمي**\n\n"
            "نقدم لكم الروم الرسمي والملف الخام الخاص بهاتف LT M50+، جاهز للتفليش.\n\n"
            "⚙️ **وضع التفليش المطلوب:**\n"
            "`Firmware Upgrade` (وضع BROM)\n\n"
            "🔐 **كلمة سر فك الضغط:**\n"
            "`Al_aidroosS1`\n"
            "*(اضغط على كلمة السر لنسخها تلقائياً)*\n\n"
            "⚠️ **تنبيه وحقوق النشر:**\n"
            "جميع الحقوق محفوظة لـ **AlaidroosSoft** وبوت **HMAX-haithamMax**.\n"
            "يمنع منعاً باتاً إعادة رفع الملف أو نقله في المواقع والقنوات الأخرى دون ذكر المصدر ورابط القناة الأصلية.\n\n"
            "━━━━━━━━━━━━━━━━━\n"
            "👇 **لتحميل الروم مباشرة وبأعلى سرعة اضغط أدناه:**"
        )
        
        bot.edit_message_text(
            display_text, user_id, call.message.message_id, 
            reply_markup=markup, parse_mode="Markdown"
        )
        return

    elif cd == "page_rare_lt_free_1":
        if 'track_tool' in globals(): track_tool("أنظمة LT مجانية رقم 1", user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("📥 تحميل المجموعة 1",
                url="https://mega.nz/folder/fQlhyBgL#FMgONMNH-gVwX9-tGJ2ZDw"),
            types.InlineKeyboardButton("🔙 رجوع", callback_data="rare_brand_مجانية_LT"),
        )
        bot.edit_message_text(hmaxi18n.translate_static_content("lt_free_1", LT_FREE_1_DESC, hmaxi18n.get_language(user_id)), user_id, call.message.message_id,
                              reply_markup=markup, parse_mode="Markdown")
        return

    elif cd == "page_rare_lt_free_2":
        if 'track_tool' in globals(): track_tool("أنظمة LT مجانية رقم 2", user_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("📥 تحميل المجموعة 2",
                url="https://mega.nz/folder/FJRyFKoa#Z-T-obZUkQ4RB-AxkAtseg"),
            types.InlineKeyboardButton("🔙 رجوع", callback_data="rare_brand_مجانية_LT"),
        )
        bot.edit_message_text(hmaxi18n.translate_static_content("lt_free_2", LT_FREE_2_DESC, hmaxi18n.get_language(user_id)), user_id, call.message.message_id,
                              reply_markup=markup, parse_mode="Markdown")
        return

    # ===== قسم أنظمة ZTE المجانية وتفريعاتها =====
    elif cd == "rare_brand_مجانية_ZTE":
        try: bot.answer_callback_query(call.id)
        except: pass
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("📥 ZTE note 13 pro", callback_data="page_rare_zte_note13pro"),
            types.InlineKeyboardButton("🔙 رجوع لشركات الأنظمة", callback_data="rare_free_list")
        )
        bot.edit_message_text(
            "📂 **أنظمة ZTE المجانية:**\nاختر الفلاشة المطلوبة أدناه:",
            user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown"
        )
        return

    # 🌟 معالج صفحة الفلاشة الحصرية ZTE note 13 pro (عرض الصورة والنص)
    elif cd == "page_rare_zte_note13pro":
        try: bot.answer_callback_query(call.id)
        except: pass
        if 'track_tool' in globals(): track_tool("فلاشة ZTE note 13 pro", user_id)
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("📥 رابط التنزيل (Mega)", url="https://mega.nz/file/bgAjhJDS#6azySPETc9n4CshVP1SDBa-hGMCktiQ1u3m9kdpDK8k"),
            types.InlineKeyboardButton("🔙 رجوع لقائمة ZTE", callback_data="rare_brand_مجانية_ZTE")
        )
        
        display_text = (
            "📱 **فلاشة هاتف ZTE note 13 pro**\n\n"
            "🔥 حسب طلب الإخوة المبرمجين، فلاشه الهاتف العنيد **ZTE note 13 pro** الذي ينضرب النظام تبعه أثناء الفورمات أو التخطي.\n\n"
            "📌 **ملاحظة هامة:**\n"
            "الفلاشة رسمية من شركة ZTE nubia Yemen وليست مسحوبة! وقد تم تجربتها بنجاح على أكثر من هاتف، ومن ضمنهم هاتف أحد عملاء (زيد فون للهواتف الذكية).\n\n"
            "💐 **منقولة من الأخ:** توفيق الحمامي\n"
            "🤲 *دعوة في ظهر الغيب ولكم مثلها*\n"
            "━━━━━━━━━━━━━━━━━\n"
            "👇 **لتحميل الروم مباشرة وبأعلى سرعة اضغط أدناه:**"
        )
        
        # استخدام إرسال الصورة مع حذف الرسالة النصية القديمة لكي يظهر شكل الهاتف للعميل
        try:
            bot.delete_message(user_id, call.message.message_id)
            bot.send_photo(
                user_id, 
                "https://t.me/haithamMax1/1019", 
                caption=display_text, 
                reply_markup=markup, 
                parse_mode="Markdown"
            )
        except:
            bot.send_message(user_id, display_text, reply_markup=markup, parse_mode="Markdown")
        return


    elif cd.startswith("rare_brand_"):
        parts = cd.split("_")
        type_str, brand = parts[2], parts[3]
        if 'track_tool' in globals(): track_tool(f"أنظمة {type_str} - {brand}", user_id)
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("📱 واتساب", url=WHATSAPP_URL),
            types.InlineKeyboardButton("👤 تيلجرام", url=TELEGRAM_ADMIN),
        )
        markup.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="rare_free_list"))
        bot.edit_message_text(
            f"📂 **أنظمة {type_str} - {brand}**\n\n📞 للطلب أو الاستفسار تواصل معنا:",
            user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown"
        )
        return

    
    # ===== لوحة الإدارة =====
    elif cd == "admin_panel":
        if int(user_id) == MY_CHAT_ID:
            try:
                bot.delete_message(user_id, call.message.message_id)
            except:
                pass
            show_admin_panel(user_id)

    elif cd == "admin_stats":
        if int(user_id) == MY_CHAT_ID:
            show_advanced_stats(user_id, call.message.message_id)

    elif cd == "admin_daily_stats" or cd == "refresh_daily_stats":
        if int(user_id) == MY_CHAT_ID:
            try:
                bot.delete_message(user_id, call.message.message_id)
            except:
                pass
            show_daily_stats(user_id)

    elif cd == "admin_list_users":
        if int(user_id) == MY_CHAT_ID:
            show_admin_users_list(user_id, call.message.message_id)

    elif cd == "admin_ban_user":
        if int(user_id) == MY_CHAT_ID:
            msg = bot.send_message(user_id, "🚫 أرسل آيدي المستخدم لحظره (أو 'إلغاء'):")
            bot.register_next_step_handler(msg, process_ban_user)

    elif cd == "admin_unban_user":
        if int(user_id) == MY_CHAT_ID:
            msg = bot.send_message(user_id, "✅ أرسل آيدي المستخدم لفك حظره (أو 'إلغاء'):")
            bot.register_next_step_handler(msg, process_unban_user)

    elif cd.startswith("ban_user_"):
        if int(user_id) == MY_CHAT_ID:
            target_id = cd.replace("ban_user_", "")
            set_user_ban_status(user_id, target_id, 1, call.message.message_id)

    elif cd.startswith("unban_user_"):
        if int(user_id) == MY_CHAT_ID:
            target_id = cd.replace("unban_user_", "")
            set_user_ban_status(user_id, target_id, 0, call.message.message_id)

    elif cd == "admin_all_requests":
        if int(user_id) == MY_CHAT_ID:
            show_all_user_requests(user_id, call.message.message_id)

    elif cd.startswith("reply_req_"):
        target_id = cd.replace("reply_req_", "")
        msg = bot.send_message(user_id, f"💬 أرسل الرد للمستخدم `{target_id}`:", parse_mode="Markdown")
        bot.register_next_step_handler(msg, send_reply_to_user, target_id)

    elif cd == "admin_broadcast":
        if int(user_id) == MY_CHAT_ID:
            msg = bot.send_message(user_id, "📢 أرسل الرسالة للتعميم (أو 'إلغاء'):")
            bot.register_next_step_handler(msg, perform_broadcast)

    elif cd == "admin_update_notify":
        if int(user_id) == MY_CHAT_ID:
            perform_auto_update_notification(user_id)

   # ===== معالج الروابط العام (آخر فرع) =====
    elif cd.startswith("link_"):
        try: bot.answer_callback_query(call.id)
        except: pass
        
        found = False
        category, tool_name, link = "", "", ""
        for cat in DATA.keys():
            prefix = f"link_{cat}_"
            if cd.startswith(prefix):
                key = cd.replace(prefix, "")
                if key in DATA[cat]:
                    category = cat
                    value = DATA[cat][key]
                    tool_name = value[0] if isinstance(value, (list, tuple)) and len(value) > 0 else str(value)
                    link = value[1] if isinstance(value, (list, tuple)) and len(value) > 1 else ""
                    found = True
                    break
        if not found:
            bot.answer_callback_query(call.id, "❌ لم يتم العثور على الأداة.", show_alert=True)
            return
        
        if 'track_tool' in globals(): track_tool(tool_name, user_id)
        
        # خريطة الأوصاف المخصصة لمنع ظهور الروابط كنصوص عادية ومكسورة
        descriptions_map = {
            "mobimover": MOBIMOVER_DESC,
            "maxtech_vip": MAXTECH_VIP_DESC,
            "samfw": "🛠️ **Samfw tool المحدثة**\n\nأفضل أداة مجانية لعمليات السوفت وير وبثغرة الـ MTP بضغطة زر.\n\nالتحميل متاح بالأسفل:",
            
            "tsm_edition": TSM_EDITION_DESCRIPTION,

            "activator_master": (
                "💻 **أداة Activator Master v8.0 العملاقة:**\n\n"
                "أداة شاملة وممتازة لإدارة وتنشيط نظام الويندوز وحل مشاكله بضغطة زر واحدة.\n\n"
                "📌 **أبرز ميزات ووظائف الأداة:**\n"
                "• **تنشيط وتفعيل الويندوز:** تفعيل مجاني ومستقر لجميع إصدارات Windows و Microsoft Office.\n"
                "• **التحكم في التحديثات:** إيقاف تحديثات الويندوز نهائياً أو إعادتها لمنع استهلاك الإنترنت المفاجئ.\n"
                "• **أدوات إضافية:** تنظيف النظام، تسريع الأداء، وإدارة المهام المتقدمة.\n\n"
                "🔐 **كلمة سر فك ضغط الملف:** `Morocco`\n"
                "━━━━━━━━━━━━━━━━━\n"
                "📥 للتحميل المباشر والسريع، اضغط أدناه:"
            ),
            
            "defender_control": (
                "🛡️ **أداة Defender Control v2.1:**\n\n"
                "أداة صغيرة وفعالة جداً لإيقاف أو تشغيل مكافح الفيروسات (Windows Defender) بضغطة زر واحدة، لتسهيل عملك أثناء استخدام الكراكات والأدوات البرمجية بدون أن يتم حذفها.\n\n"
                "━━━━━━━━━━━━━━━━━\n"
                "📥 للتحميل المباشر والسريع، اضغط أدناه:"
            ),
            
            "honor_fastboot": (
                "🔍 **أداة قراءة معلومات الهونر (Fastboot):**\n\n"
                "أداة متخصصة ومميزة لقراءة كافة تفاصيل ومعلومات هواتف Honor في وضع الـ Fastboot بسهولة وسرعة فائقة.\n\n"
                "━━━━━━━━━━━━━━━━━\n"
                "📥 للتحميل المباشر والسريع، اضغط أدناه:"
            )
        }
        
        # 🛡️ الحماية السحرية: تنظيف اسم الأداة من الشرطات السفلية لمنع تكسر الماركداون
        safe_tool_name = tool_name.replace("_", " ")
        
        display_text = hmaxi18n.translate_static_content(
            key, descriptions_map.get(key, f"✨ **{safe_tool_name}**\n\nإليك زر التحميل المباشر والآمن للأداة المطلوبة:"),
            hmaxi18n.get_language(user_id),
        )
        
        back_map = {
            "free_iphone": "main_free_tools", 
            "free_android": "main_free_tools", 
            "iphone_tools": "main_free_tools", 
            "tools": "main_tools", 
            "drivers": "main_drivers", 
            "unlocking": "main_unlocking", 
            "firmware_sites": "main_firmware_sites"
        }
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        if link.startswith("http"):
            markup.add(types.InlineKeyboardButton("⬇️ اضغط للتحميل المباشر", url=link))
        markup.add(types.InlineKeyboardButton("🔙 رجوع", callback_data=back_map.get(category, "back_start")))
        
        try:
            bot.edit_message_text(display_text, user_id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        except Exception as e:
            print(f"Error in link handler: {e}")
        return

# ================= 10. دوال الطلبات والإدارة =================

def handle_user_request(message, request_type):
    user_id = message.chat.id
    if is_user_banned(user_id):
        bot.reply_to(message, "🚫 تم حظرك من استخدام النظام.")
        return
    username = message.from_user.username or "NoUsername"
    request_text = f"[{request_type}] {message.text}"
    try:
        if db:
            db.collection('user_requests').add({
                "user_id": user_id,
                "user_name": username,
                "request_text": request_text,
                "request_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                "status": "pending",
            })
            db.collection('stats').document('requests').set(
                {'value': firestore.Increment(1)}, merge=True
            )
            increment_daily_stat('requests')
    except Exception as e:
        print(f"خطأ في تسجيل الطلب: {e}")

    # 🆕 منح نقاط الطلب مع حد يومي لمنع الاستغلال
    rewarded_request = hmaxx.award_request_reward(user_id, POINTS_PER_ACTION["request"])
    if not rewarded_request:
        log_interaction(user_id, "طلب بدون مكافأة إضافية (تم بلوغ الحد اليومي)")
    log_interaction(user_id, request_type)

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("💬 رد مباشر", callback_data=f"reply_req_{user_id}"))
    bot.send_message(
        MY_CHAT_ID,
        f"📩 **طلب جديد:**\n\n👤 المستخدم: {username} (`{user_id}`)\n📝 الطلب: {request_text}",
        reply_markup=markup, parse_mode="Markdown"
    )
    bot.send_message(
        user_id,
        f"✅ تم إرسال طلبك بنجاح!\n"
        f"💎 حصلت على **+{POINTS_PER_ACTION['request']} نقاط**\n"
        f"📞 سيتم الرد عليك قريباً.",
        parse_mode="Markdown"
    )
    show_main_menu(user_id)


def send_reply_to_user(message, target_id):
    try:
        if message.content_type == 'text':
            bot.send_message(target_id, f"💬 **رد من الإدارة:**\n\n{message.text}", parse_mode="Markdown")
        else:
            bot.copy_message(target_id, message.chat.id, message.message_id,
                             caption="💬 رد من الإدارة:")
        bot.send_message(MY_CHAT_ID, f"✅ تم إرسال الرد للمستخدم `{target_id}` بنجاح.", parse_mode="Markdown")
    except Exception as e:
        bot.send_message(MY_CHAT_ID, f"❌ فشل إرسال الرد: {str(e)}")


def show_admin_panel(chat_id):
    """لوحة تحكم الأدمن المحدّثة"""
    total = 0
    banned = 0
    try:
        if db:
            total = db.collection('users').count().get()[0][0].value
            banned = db.collection('users').where('is_banned', '==', 1).count().get()[0][0].value
    except Exception as e:
        print(f"خطأ في الإحصائيات: {e}")

    text = (
        f"⚙️ **لوحة التحكم - HMAX Admin**\n"
        f"━━━━━━━━━━━━━━━━━━\n\n"
        f"👥 إجمالي المستخدمين: `{total}`\n"
        f"🚫 المحظورين: `{banned}`\n"
        f"📅 التاريخ: `{datetime.date.today()}`"
    )
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📊 إحصائيات يومية", callback_data="admin_daily_stats"),
        types.InlineKeyboardButton("📈 إحصائيات متقدمة", callback_data="admin_stats"),
    )
    markup.add(
        types.InlineKeyboardButton("📩 طلبات المستخدمين", callback_data="admin_all_requests"),
        types.InlineKeyboardButton("👥 قائمة المستخدمين", callback_data="admin_list_users"),
    )
    markup.add(
        types.InlineKeyboardButton("🚫 حظر مستخدم", callback_data="admin_ban_user"),
        types.InlineKeyboardButton("✅ فك حظر", callback_data="admin_unban_user"),
    )
    markup.add(
        types.InlineKeyboardButton("📢 إرسال جماعي", callback_data="admin_broadcast"),
        types.InlineKeyboardButton("🆕 نشر التحديثات", callback_data="admin_update_notify"),
    )
    markup.add(
        types.InlineKeyboardButton("🏥 فحص صحة المكتبة", callback_data="admin_dump_health"),
    )
    markup.add(types.InlineKeyboardButton("🏠 رجوع للقائمة", callback_data="back_start"))
    bot.send_message(chat_id, text, reply_markup=markup, parse_mode="Markdown")


def show_admin_users_list(chat_id, message_id=None):
    users = []
    try:
        if db:
            docs = db.collection('users').order_by(
                'joined_date', direction=firestore.Query.DESCENDING
            ).limit(50).stream()
            for doc in docs:
                users.append(doc.to_dict())
    except Exception as e:
        print(f"خطأ في جلب المستخدمين: {e}")

    markup = types.InlineKeyboardMarkup(row_width=1)
    if not users:
        text = "👥 **قائمة المستخدمين**\n\nلا يوجد مستخدمون."
    else:
        lines = ["👥 **آخر 50 مستخدم:**\n━━━━━━━━━━━━━━━━━━\n"]
        for u in users:
            uid = u.get('id')
            full_name = u.get('full_name', 'غير معروف')
            username = u.get('username')
            is_banned = u.get('is_banned', 0)
            points = u.get('points', 0)
            rank_name, _ = get_rank(points)
            status = "🚫 محظور" if is_banned == 1 else "✅ نشط"
            uname_text = f"@{username}" if username and username != "NoUsername" else "—"
            lines.append(f"▫️ {full_name} ({uname_text})\n   🆔 `{uid}` | 💎 {points} | {rank_name} | {status}")
            if uid == MY_CHAT_ID:
                continue
            if is_banned == 1:
                markup.add(types.InlineKeyboardButton(f"✅ فك حظر {full_name}", callback_data=f"unban_user_{uid}"))
            else:
                markup.add(types.InlineKeyboardButton(f"🚫 حظر {full_name}", callback_data=f"ban_user_{uid}"))
        text = "\n".join(lines)

    markup.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="admin_panel"))
    if message_id:
        try:
            bot.edit_message_text(text, chat_id, message_id, reply_markup=markup, parse_mode="Markdown")
        except:
            bot.send_message(chat_id, text, reply_markup=markup, parse_mode="Markdown")
    else:
        bot.send_message(chat_id, text, reply_markup=markup, parse_mode="Markdown")


def set_user_ban_status(admin_id, target_id, status, message_id=None):
    try:
        target_id = int(target_id)
    except ValueError:
        bot.send_message(admin_id, "❌ الآيدي غير صحيح.")
        show_admin_panel(admin_id)
        return

    if target_id == MY_CHAT_ID:
        bot.send_message(admin_id, "⛔ لا يمكن حظر حساب الإدارة.")
        show_admin_panel(admin_id)
        return

    try:
        user_ref = db.collection('users').document(str(target_id))
        user_doc = user_ref.get()
        if not user_doc.exists:
            bot.send_message(admin_id, "❌ المستخدم غير موجود في قاعدة البيانات.")
            show_admin_panel(admin_id)
            return
        # مزامنة الحظر مع Firebase والملف المحلي حتى تكون كل مسارات الإدارة متطابقة.
        operation_ok = (
            ban_user_id(target_id)
            if status == 1
            else unban_user_id(target_id)
        )
        if not operation_ok:
            bot.send_message(
                admin_id,
                "⚠️ تعذر حفظ تغيير الحظر في Firebase. تم الإبقاء على الحظر المحلي.",
            )
            if message_id:
                show_admin_users_list(admin_id, message_id)
            return
    except Exception as e:
        bot.send_message(admin_id, f"❌ خطأ: {e}")
        return

    if status == 1:
        bot.send_message(admin_id, f"🚫 تم حظر المستخدم `{target_id}`.", parse_mode="Markdown")
        try:
            bot.send_message(target_id, "🚫 تم حظرك من البوت بواسطة الإدارة.")
        except:
            pass
    else:
        bot.send_message(admin_id, f"✅ تم فك حظر المستخدم `{target_id}`.", parse_mode="Markdown")
        try:
            bot.send_message(target_id, "✅ تم فك الحظر عنك، يمكنك استخدام البوت الآن.")
        except:
            pass

    if message_id:
        try:
            show_admin_users_list(admin_id, message_id)
        except:
            show_admin_panel(admin_id)


def process_ban_user(message):
    if int(message.chat.id) != MY_CHAT_ID:
        return
    if message.text and message.text.strip() == "إلغاء":
        show_admin_panel(message.chat.id)
        return
    set_user_ban_status(message.chat.id, message.text.strip(), 1)


def process_unban_user(message):
    if int(message.chat.id) != MY_CHAT_ID:
        return
    if message.text and message.text.strip() == "إلغاء":
        show_admin_panel(message.chat.id)
        return
    set_user_ban_status(message.chat.id, message.text.strip(), 0)


def show_all_user_requests(chat_id, message_id=None):
    reqs = []
    try:
        if db:
            docs = db.collection('user_requests').order_by(
                'request_date', direction=firestore.Query.DESCENDING
            ).limit(50).stream()
            for doc in docs:
                reqs.append(doc.to_dict())
    except Exception as e:
        print(f"خطأ في جلب الطلبات: {e}")

    if not reqs:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="admin_panel"))
        if message_id:
            bot.edit_message_text("📩 لا توجد طلبات حالياً.", chat_id, message_id, reply_markup=markup)
        else:
            bot.send_message(chat_id, "📩 لا توجد طلبات حالياً.", reply_markup=markup)
        return

    if message_id:
        try:
            bot.delete_message(chat_id, message_id)
        except:
            pass

    bot.send_message(chat_id, "📩 **آخر 50 طلب:**", parse_mode="Markdown")
    for r in reqs:
        uid = r.get('user_id')
        uname = r.get('user_name', 'غير معروف')
        text = r.get('request_text', '')
        date = r.get('request_date', '')
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(f"💬 رد على {uname}", callback_data=f"reply_req_{uid}"))
        bot.send_message(
            chat_id,
            f"👤 {uname} (`{uid}`)\n🕐 {date}\n📝 {text}",
            reply_markup=markup, parse_mode="Markdown"
        )
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔙 رجوع للوحة الإدارة", callback_data="admin_panel"))
    bot.send_message(chat_id, "💡 اضغط على زر الرد أسفل أي طلب.", reply_markup=markup)


def show_all_user_requests_simple(chat_id):
    """نسخة مبسطة من الكيبورد السفلي"""
    show_all_user_requests(chat_id)


def perform_broadcast(message):
    """منع تداخل الرسائل ومقاطعة الإرسال عن طريق إطلاق خيط خلفي مستقل فوراً 🚀"""
    if int(message.chat.id) != MY_CHAT_ID:
        return
    if message.text and message.text.strip() == "إلغاء":
        show_admin_panel(message.chat.id)
        return
        
    # Keep bulk sends serialized so concurrent admins cannot exceed Telegram's shared rate limit.
    _start_broadcast_worker(_run_broadcast_async_worker, (message,), MY_CHAT_ID)


def _run_broadcast_async_worker(message):
    """Send a broadcast in bounded Firestore pages with a conservative rate limit."""
    status_msg = bot.send_message(
        MY_CHAT_ID,
        "📢 بدأ الإرسال على دفعات وبسرعة آمنة. ستظهر تحديثات التقدم هنا.",
        parse_mode="HTML",
    )
    counters = {"sent": 0, "failed": 0, "blocked": 0, "processed": 0}
    started_at = time.time()
    scan_error = ""

    def update_progress():
        try:
            bot.edit_message_text(
                f"📢 <b>جاري الإرسال على دفعات</b>\n\n"
                f"📊 تمت معالجة: <code>{counters['processed']}</code>\n"
                f"✅ نجح: <code>{counters['sent']}</code>\n"
                f"❌ فشل: <code>{counters['failed']}</code>",
                MY_CHAT_ID,
                status_msg.message_id,
                parse_mode="HTML",
            )
        except Exception:
            pass

    try:
        for uid in iter_active_user_ids():
            final_error = None
            try:
                bot.copy_message(uid, message.chat.id, message.message_id)
                counters["sent"] += 1
            except Exception as send_error:
                final_error = send_error
                error_text = str(send_error).lower()
                if any(word in error_text for word in (
                    "blocked", "deactivated", "not found", "chat not found"
                )):
                    counters["blocked"] += 1

                retry_match = re.search(r"retry after (\d+)", error_text)
                if retry_match:
                    time.sleep(int(retry_match.group(1)) + 1)
                    try:
                        bot.copy_message(uid, message.chat.id, message.message_id)
                        counters["sent"] += 1
                        final_error = None
                    except Exception as retry_error:
                        final_error = retry_error

                if final_error is not None:
                    counters["failed"] += 1

            counters["processed"] += 1
            if counters["processed"] % 50 == 0:
                update_progress()
            # Keep headroom below Telegram's shared bot broadcast limit.
            time.sleep(0.05)
    except Exception as scan_exception:
        scan_error = str(scan_exception)[:250]
        print(f"تعذر إكمال بث المستخدمين: {scan_exception}")

    processed = counters["processed"]
    success_rate = (counters["sent"] / processed * 100) if processed else 0
    final_report = (
        f"✅ <b>انتهى الإرسال الجماعي</b>\n"
        f"━━━━━━━━━━━━━━━━━━\n\n"
        f"👥 <b>تمت معالجة:</b> <code>{processed}</code>\n"
        f"✅ <b>تم الإرسال:</b> <code>{counters['sent']}</code>\n"
        f"❌ <b>فشل:</b> <code>{counters['failed']}</code>\n"
        f"🚫 <b>حظر البوت:</b> <code>{counters['blocked']}</code>\n"
        f"📊 <b>نسبة النجاح:</b> <code>{success_rate:.1f}%</code>\n"
        f"⏱️ <b>المدة:</b> <code>{int(time.time() - started_at)}</code> ثانية"
    )
    if scan_error:
        safe_error = telebot.util.escape_html(scan_error)
        final_report += f"\n⚠️ <b>توقف المسح قبل اكتماله:</b> <code>{safe_error}</code>"
    if processed == 0 and not scan_error:
        final_report += "\n⚠️ لا يوجد مستخدمون نشطون للإرسال."
    try:
        bot.edit_message_text(final_report, MY_CHAT_ID, status_msg.message_id, parse_mode="HTML")
    except Exception:
        bot.send_message(MY_CHAT_ID, final_report, parse_mode="HTML")


def perform_auto_update_notification(chat_id):
    """Run update notification asynchronously without overlapping another broadcast."""
    _start_broadcast_worker(
        _perform_auto_update_notification_worker,
        (chat_id,),
        chat_id,
    )


def _perform_auto_update_notification_worker(chat_id):
    notified = set()
    try:
        if db:
            for page in hmaxruntime.iter_document_pages(
                db.collection("notified_items"), page_size=200
            ):
                for doc in page:
                    data = doc.to_dict() or {}
                    notified.add((data.get("category"), data.get("item_key")))
    except Exception as e:
        print(f"تعذر قراءة سجل الإشعارات: {e}")

    new_items = []
    cat_names = {
        "tools": "تحديثات الادوات",
        "drivers": "التعريفات",
        "unlocking": "فك الشفرات",
        "iphone_tools": "أدوات الآيفون",
        "free_android": "أدوات أندرويد مجانية",
        "free_iphone": "أدوات آيفون مجانية",
        "firmware_sites": "مواقع الأنظمة",
        "ai_offers": "عروض الذكاء الاصطناعي",
    }

    for category, items in DATA.items():
        category_name = cat_names.get(category, category)
        for item_key, value in items.items():
            if (category, item_key) not in notified:
                new_items.append(f"▫️ {value[0]} (في {category_name})")
                if db:
                    try:
                        db.collection("notified_items").document(
                            f"{category}_{item_key}"
                        ).set(
                            {"category": category, "item_key": item_key},
                            merge=True,
                        )
                    except Exception as e:
                        print(f"تعذر تسجيل الإضافة {category}/{item_key}: {e}")

    if not new_items:
        bot.send_message(chat_id, "ℹ️ لا توجد إضافات جديدة حالياً.")
        return

    message_text = "🆕 **تحديثات جديدة في HMAX!**\n\n✨ تمت إضافة:\n\n" + "\n".join(new_items)
    bot.send_message(
        chat_id,
        f"🆕 اكتُشف {len(new_items)} إضافة. بدأ الإرسال على دفعات...",
    )
    sent = 0
    failed = 0
    processed = 0
    scan_error = ""
    try:
        for uid in iter_active_user_ids():
            processed += 1
            try:
                bot.send_message(uid, message_text, parse_mode="Markdown")
                sent += 1
            except Exception:
                failed += 1
            time.sleep(0.05)
    except Exception as e:
        scan_error = str(e)[:200]
        print(f"تعذر إكمال إشعار التحديثات: {e}")

    try:
        bot.send_message(chat_id="@haithamMax1", text=message_text, parse_mode="Markdown")
    except Exception as channel_error:
        print(f"❌ خطأ أثناء النشر للقناة: {channel_error}")

    final_text = (
        f"✅ انتهى النشر على {processed} مستخدم.\n"
        f"📤 نجح: {sent}\n❌ فشل: {failed}"
    )
    if scan_error:
        final_text += f"\n⚠️ توقف مسح المستخدمين: {scan_error}"
    bot.send_message(chat_id, final_text)


# ================= 🆕 نظام الرد المباشر بضغطة Reply الذكي (نسخة واحدة نظيفة) =================
@bot.message_handler(func=lambda m: m.chat.id == MY_CHAT_ID and m.reply_to_message)
def admin_reply_to_user(message):
    """إرسال رد الإدارة عند استخدام Reply على رسالة تحتوي على آيدي المستخدم."""
    import re
    reply_text = message.reply_to_message.caption or message.reply_to_message.text or ""

    # يدعم الصيغ الحالية مثل: ID: 123456 أو الآيدي (ID): 123456،
    # وكذلك رسائل الطلبات التي تحتوي على الآيدي بين قوسين.
    user_id_match = re.search(r'(?:ID|الآيدي)[^0-9]{0,40}(\d{5,})', reply_text, re.IGNORECASE)
    if not user_id_match:
        user_id_match = re.search(r'[^0-9](\d{5,})[^0-9]', f" {reply_text} ")

    if not user_id_match:
        bot.reply_to(message, "❌ لم أجد آيدي المستخدم في الرسالة الأصلية المعلق عليها.")
        return

    target_id = user_id_match.group(1)
    try:
        if message.content_type == "text":
            safe_text = telebot.util.escape_html(message.text or "")
            bot.send_message(
                int(target_id),
                f"✅ <b>رد مباشر من الإدارة:</b>\n\n{safe_text}",
                parse_mode="HTML"
            )
        else:
            bot.copy_message(int(target_id), message.chat.id, message.message_id, caption="💬 رد من الإدارة:")
        bot.reply_to(message, "✅ تم إرسال الرد للمستخدم بنجاح! 🚀")
    except Exception as e:
        bot.reply_to(message, f"❌ فشل الإرسال للمستخدم: {e}")

# ================= 🧠 طبقة تطوير HMAX المتقدمة =================
try:
    hmaxx.install(bot, db, DATA, MY_CHAT_ID)
except Exception as e:
    print(f"⚠️ تعذر تحميل طبقة تطوير HMAX: {e}")
try:
    hmaxpro.install(bot, db, MY_CHAT_ID)
except Exception as e:
    print(f"⚠️ تعذر تحميل طبقة HMAX PRO: {e}")
try:
    import hmax_dump_tools
    hmax_dump_tools.install(bot, db, DATA, MY_CHAT_ID)
except Exception as e:
    print(f"⚠️ تعذر تحميل طبقة DUMP Tools: {e}")
try:
    import hmax_dump_advanced
    hmax_dump_advanced.install(bot, db, MY_CHAT_ID)
except Exception as e:
    print(f"⚠️ تعذر تحميل طبقة DUMP Advanced: {e}")

# ================= 11. تشغيل البوت =================
def run_bot():
    print("🚀 جاري تهيئة البوت...")
    try:
        bot.remove_webhook()
    except Exception as e:
        print(f"⚠️ تنبيه: {e}")

    try:
        set_bot_commands()
    except Exception as e:
        print(f"⚠️ تعذر إعداد أوامر البوت: {e}")
    print("✅ البوت يعمل الآن!")
    bot.infinity_polling(timeout=20, long_polling_timeout=20)
def _handle_dump_search(message):
    user_id = message.chat.id
    query = (message.text or "").strip()
    if query in ("إلغاء", "cancel", "/cancel"):
        show_main_menu(user_id)
        return
    import hmax_dump_advanced as _adv
    from telebot import types as _types
    results = _adv.search_cards(query)
    lang = hmaxi18n.get_language(user_id)

    if not results:
        bot.send_message(user_id, f"🔍 لم أجد نتائج عن: {query}")
        return

    mk = _types.InlineKeyboardMarkup(row_width=1)
    for r in results[:20]:
        sk = _adv._register_card_for_nav(r["tool_key"], r["cb"])
        if sk:
            mk.add(_types.InlineKeyboardButton(
                f"{r['icon']} {r['label']}"[:60],
                callback_data=f"dumptoolcard_{sk}",
            ))
    mk.add(_types.InlineKeyboardButton("🔙 رجوع", callback_data="dump_tools_section"))
    bot.send_message(user_id, f"🔍 نتائج البحث عن: *{query}*", reply_markup=mk, parse_mode="Markdown")

if __name__ == "__main__":
    bot_thread = Thread(target=run_bot, daemon=True)
    bot_thread.start()
    run_flask()
