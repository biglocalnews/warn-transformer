import typing
from datetime import datetime

from ..schema import BaseTransformer


class Transformer(BaseTransformer):
    # class Transformer:
    """Transform Michigan raw data for consolidation."""

    postal_code = "MI"
    fields = dict(
        company="company",
        location="city",  # Should it be county? Concatenate with county?
        effective_date="date_start",
        jobs="jobs",
    )
    date_format = ["%m/%d/%Y", "%B %d, %Y", "%B %d, %y"]
    date_corrections = {
        "June 17, 2024 - July 31, 2024": datetime(2024, 6, 17),
        "Commencing June 2025": datetime(2025, 6, 1),
        "Beginning April 12, 2025": datetime(2025, 4, 12),
        "June 30, 2024 (approximate)": datetime(2024, 6, 30),
        "Beginning February 2, 2025": datetime(2025, 2, 2),
        "Beginning April 21, 2025": datetime(2025, 4, 21),
        "Beginning February 6, 2025": datetime(2025, 2, 6),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020c/2020-07-27_WARN_VitalCare-Inc.pdf?rev=2ebd10fd57e240d59dac5b47034fa3d7": datetime(
            2020, 9, 27
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2022/2022-04-13_WARN_Entergy-Palisades-Nuclear-Plant.pdf?rev=de7ed4d284db41d988eb68a37fc7d3dc": datetime(
            2022, 6, 24
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2022/2022-09-16_WARN_Second-Samuel-Transport.pdf?rev=fb102bdb5a3b4c9abf8b9c2b114cc430": datetime(
            2022, 11, 8
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2023/2023-04-21_WARN_Dawson-Manufacturing-Company.pdf?rev=84268e047a3c4dd08b09c0c07147e005": datetime(
            2023, 7, 1
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2023/2023-05-01_WARN_Lear-Corporation_Davison-Plant.pdf?rev=3447f62a22a241c1b70275d329b1a107": datetime(
            2023, 6, 30
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2022/2022-09-29_WARN_DETDSP.pdf?rev=b38245c99c10431cbc8a564159b41923": datetime(
            2022, 9, 30
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2022/2022-12-14_WARN_Amerifirst-Home-Mortgage.pdf?rev=ac28b0672bf8485d9499f7653a26a305": datetime(
            2023, 2, 12
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2023/2023-01-23_WARN-Notice_Concentrix-Corporation.pdf?rev=64fad446edf444299d1061dc7700d7da": datetime(
            2023, 3, 31
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2023/2023-06-02_WARN_Notice_-Shiloh-Industries.pdf?rev=ff420ba2087f4fabbe6e05b03fc67da0": datetime(
            2023, 5, 23
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2023/2023-03-23_WARN-Notice_Rapid-Financial-Services-LLC.pdf?rev=3f2bcea9c62c45ada943037fff88f2a6": datetime(
            2023, 3, 17
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2022/2022-02-16_WARN_Peloton.pdf?rev=b6d05142a1e640a099bdb903f7135a1a": datetime(
            2022, 2, 8
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2022/2022-10-12_FCA-US-Warren-Truck-Assembly-Plant/2022-10-12_WARN_FCA-US-Warren-Truck-Assembly-Plant.pdf?rev=5bf9398797a1405c94856c64e31a71f6": datetime(
            2022, 12, 12
        ),  # Date is in the ballpark
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2023/2023-07-12_WARN_Henry-A-Fox-Sales.pdf?rev=66fb7946ed6d4f919b88779222275c22": datetime(
            2023, 9, 15
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020b/Hertz_updated_WARN_Notice_5232020.pdf?rev=24ae228763964777aa21756b7610bdc1": datetime(
            2020, 5, 20
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020/20200420_Williams_Intl_WARN.pdf?rev=7508e61f18ea42fea38bd745284287e2": datetime(
            2020, 4, 13
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2021/2021_01-08_UAW_Chrysler_WARN.pdf?rev=675c529eb9744dbd84b5dbf0dbfc473c": None,
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020/20200430_Hertz_WARN.pdf?rev=e4d1304ab6d949ef8a923bc1de815712": datetime(
            2020, 4, 14
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020b/20200709_Holiday_Inn_GR_WARN_Notice.pdf?rev=4b1829c8c5a241bf96cdd3074c6e7809": datetime(
            2020, 6, 30
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020/2020-07-20_MotorCity_Casino_Hotel_WARN.pdf?rev=d4dc8ded496248eebb01fbc226293eea": datetime(
            2020, 9, 15
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020b/20200413_Four_Winds_Casinos_WARN.pdf?rev=4f85faa7faf64383bdec07461980ee41": datetime(
            2020, 4, 13
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020b/20200618_Staples_WARN_Notice.pdf?rev=5ced945de3c24dd9969524b776a78750": datetime(
            2020, 6, 19
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020/2020-08-17_HMSHost_WARN_no_names.pdf?rev=677f45d598ee483ba69b4842dcdf6e5d": datetime(
            2020, 10, 15
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020b/20200408_Pace_Industrices_WARN.pdf?rev=b2a38964abc344eaa1b8d5e1beff0b22": datetime(
            2020, 3, 22
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020b/20200604_Westin_Book_Caddillac_WARN.pdf?rev=4b08e40a021f444e97432f296cbb4b83": datetime(
            2020, 3, 21
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020/2020-11-19_MGM_Grand_Detroit_WARN.pdf?rev=8f6aaf7a01834b298f2df036b5909a21": datetime(
            2020, 11, 18
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020c/20200811_Sky_Chefs_DTW_WARN_Notice.pdf?rev=74236f79de634cb3ae4221a53c756417": datetime(
            2020, 10, 1
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020b/20200409_ProspectWARN.pdf?rev=410a938ee47d42d992125301b4ec9ad3": datetime(
            2020, 3, 19
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020/20200423_Visionworks_WARN.pdf?rev=5fefb05a4a1a44c58a927465ed43eacc": datetime(
            2020, 4, 4
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020/2020-09-02_WARN_-_Orlans_PC.pdf?rev=d7ceffa7bd9d4adb9926930530d9df54": datetime(
            2020, 9, 23
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020/2020-09-03_Greektown_Casino-Hotel_WARN.pdf?rev=69f46393da7d4ee18ca8364cebb20935": datetime(
            2020, 9, 28
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020b/20200601_Wireless_Vision_WARN.pdf?rev=5e66806e04b0428baeba7d8f9fdcc8f4": datetime(
            2020, 4, 30
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020/20200420_Marsh_Plating_WARN.pdf?rev=754d8a1a3dcb4337a2735cb926521f4d": datetime(
            2020, 3, 24
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020c/2020-09-17_Tennaco_WARN.pdf?rev=e36528ccfe13487eb5e9c8b82b894fc9": datetime(
            2021, 6, 15
        ),  # ish
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020/2020_WARN_Notice_State_V2.pdf?rev=e5640aaf018944f1846ac0420b83ebe6": datetime(
            2020, 3, 24
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020b/20200409_Precision_Vehicle_Solutions_WARN.pdf?rev=a7d1de1a6ce74471b6bd7d0335d4fb1b": datetime(
            2020, 3, 20
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020/20200518_Grand_River_Polishing_WARN.pdf?rev=2e28eaa7cfdd48cea05b018b475f3437": datetime(
            2020, 3, 20
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020/20200420_Tilden_Mining_WARN.pdf?rev=6344a21d47d74208b0bffe141ec3b6ca": datetime(
            2020, 4, 26
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020/2020-09-24_SP_Plus_Corp_WARN_Notice.pdf?rev=b304f366d9924cc58330b6182da808ca": datetime(
            2020, 3, 23
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020c/20200709_TownePlace_WARN_Notice.pdf?rev=822b4ac3a2d9482d9d0fab825a56b0b6": datetime(
            2020, 3, 13
        ),  # ish
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020b/20200409_Morbark_WARN.pdf?rev=95e72c91fb6a4f3fa59a04c837a40c24": datetime(
            2020, 4, 7
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020/2020-12-15_Updated_RustyBucket_WARN.pdf?rev=0b6c40673ef344d8811075dad1703b1d": datetime(
            2020, 11, 18
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020c/2020-11-24_MotorCity_Casino_WARN.pdf?rev=04de99f317824c8696aaa7627a9efb45": datetime(
            2020, 11, 18
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020/2020-12-05_Tech_Mahindra_WARN.pdf?rev=b8f9eb6d6d8340938780c83296b3f1bc": datetime(
            2021, 1, 6
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020b/20200602_Westin_Detroit_Metro_Airport_WARN_Notice.pdf?rev=d6681916f045487a9887f709c9dafe3c": datetime(
            2020, 5, 18
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020b/20200604_Marriott_Hotel_Services_WARN.pdf?rev=1ebedde528234cbeac7e2610f8521dc2": datetime(
            2020, 3, 25
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020/20200520_Townsend_Hotel_WARN.pdf?rev=afcf5ccc7de54350996bfb9bdddba0df": datetime(
            2020, 3, 16
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020c/2020-09-18_PF_Changs_China_Bistro_WARN_Notice.pdf?rev=43f467ed95bb41eba26d275471056588": datetime(
            2020, 3, 13
        ),  # ish
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2023/Davids-Bridal/2023-06-29_WARN_Davids_Bridal.pdf?rev=3ca5f1125826490eb4e5fc156acf661f": datetime(
            2023, 7, 17
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020/2020-09-30_Kroger_WARN.pdf?rev=0e5d4200b97946a9bec77381233a0fc2": datetime(
            2020, 11, 28
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020c/20200709_Hilton_Garden_Inn_WARN_Notice.pdf?rev=5e94c1549c794842a2fb30c17be8f55e": datetime(
            2020, 6, 30
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020/20200506_Great_Lakes_Specialty_Finance_WARN.pdf?rev=c8342ca76f3f474faf5d17320e8bd0c5": datetime(
            2020, 5, 1
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020/20200512_Marriott_Detroit_Livonia_WARN.pdf?rev=4de1917eb90c409fa6a588aa7227bf64": datetime(
            2020, 3, 18
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020c/2020-08-24_Vetta_LLC_WARN.pdf?rev=0300f2738e514ac5a2f12c87fbff26f3": datetime(
            2020, 8, 17
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020b/20200622_SwissportGerald_R_Ford_International_Airport_WARN.pdf?rev=06218d866b8c425399d825b436e40595": datetime(
            2020, 4, 25
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2021/2021-03-08_WARN_JDNormanIndustries.pdf?rev=a00f3dadc0a9434db1ea76d4c4cd09bc": datetime(
            2021, 4, 30
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020/20200424_Punch_Bowl_Social_WARN.pdf?rev=1e2e11298d6b4c81b86580300a86ba13": datetime(
            2020, 3, 16
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020b/20200616_JacobsenDaniels_WARN_Notice.pdf?rev=96fdd5f611b24316b1236751b3dda772": datetime(
            2020, 6, 12
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020b/20200720_Leadec_WARN.pdf?rev=6b62fff17bf6480bbd9ea1177ab2bdf6": datetime(
            2020, 8, 31
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020/20200522_Marriott_Auburn_Hills_Pontiac_WARN.pdf?rev=a26034c66f5a4bf182b330817c9a5d63": datetime(
            2020, 5, 31
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020b/20200723_MotorCity_Casino_Hotel_WARN.pdf?rev=87c44b485e0b4fb580d78947438bf5b6": datetime(
            2020, 7, 31
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020b/20200409_Hooters_WARN.pdf?rev=74b227f87fbe42e18fd91eb91591c72d": datetime(
            2020, 3, 16
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020/Walbro_LLC__WARN_Notice_20200526.pdf?rev=f00602a0acd24b23ad6b472133473813": datetime(
            2020, 3, 24
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020/2020-10-07_LansingEntertain_WARN.pdf?rev=e38d1d2729174751bc59da437085687f": datetime(
            2020, 4, 3
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020/2020-12-21_NBHX_Trim_USA_WARN.pdf?rev=17ba9d4f9cb347de898c758c72000b08": datetime(
            2021, 1, 18
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020/20200505_MGM_Grand_WARN.pdf?rev=ff136f59e59b47e287ed6354ad6a9076": datetime(
            2020, 3, 2
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020/20200415_Wolverine_Corporation_WARN.pdf?rev=bea449562bf74a489ffd88ddd89d0d8f": datetime(
            2020, 4, 15
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2021/2021-06-07_Progenity_WARN.pdf?rev=afc8e375123e42b9aab9b66779a3db40": datetime(
            2021, 8, 6
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020b/20200716_3rdUpdated_IAC_Alma_WARN.pdf?rev=a26a934f69a2411ebe88b16e27d61829": datetime(
            2020, 7, 17
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020/20200424_Schafer_Woodworks_WARN.pdf?rev=5523b6e3e6a249ee97bfe59496b4c5aa": datetime(
            2020, 3, 24
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020b/20200707_Updated_Spire_WARN.pdf?rev=6857a98b59e34c269d567657b00cd9e9": datetime(
            2020, 7, 1
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020c/20200616_Jacobsen_Daniels_WARN_Notice.pdf?rev=58027249107a43ea9ec99918b7967c98": datetime(
            2020, 6, 12
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2023/2023-06-05_WARN_Notice_Advanced-Vehicle-Assemblies.pdf?rev=6102f06253c94135bba3d2f016d36d1e": datetime(
            2023, 7, 31
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2022/2022-11-10_WARN-Notice_PACE-Industries.pdf?rev=0d15eb4beda548afac06752cd6eb95da": datetime(
            2022, 12, 20
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2023/2023-01-17_WARN-Notice_Inteva-Products-Inc.pdf?rev=149555cccae9497cabc1bfcf356170cf": datetime(
            2023, 3, 4
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2022/2022-10-27_WARN_Argo-AI-LLC.pdf?rev=768a949046e540b3aec4d921444b5fab": datetime(
            2022, 11, 1
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2022/2022_8-30_WARN_NBHX-TRIM-CORPORATION.pdf?rev=0b76d5cdf3e9464bac73f850deb3db62": datetime(
            2022, 10, 28
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2022/2022-01-25_WARN_Penske.pdf?rev=9713da5696034aed8f0dc595ad3ff31a": datetime(
            2022, 3, 26
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2022/2022-07-29_WARN_Resonetics-LLC.pdf?rev=4be61dae754d4fb18755cbff38319840": datetime(
            2022, 9, 30
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2023/2023-03-24_WARN-Notice_EYM-King-of-Michigan-LLC.pdf?rev=c5fc3cd263324266b2864653de8fa465": datetime(
            2023, 3, 17
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2022/202261_Jervis-B-Webb-DAIFUKU-WARN-received-without-names.pdf?rev=8add1a8abac848278a041c01701b8c3c": datetime(
            2022, 8, 1
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2023/2023-06-30_WARN_FCA-US-LLC-Dundee-Engine-Plant.pdf?rev=98daaba691664f83823ea98bf4aa15a1": datetime(
            2023, 9, 3
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2023/2023-03-20_WARN-Notice_Prospect.pdf?rev=7e345588a17d4fb6976c128f6f3d9a36": datetime(
            2023, 5, 1
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2023/2023-10-04_WARN-Notice_Sodecia-Automotive.pdf?rev=b09c0f021b6d4f16a917c9f74a53a854": datetime(
            2023, 9, 25
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2023/2023-03-16_WARN-Notice_Function-Inc.pdf?rev=c0395c802e704be8b41d6ab5a98b7fd9": datetime(
            2023, 5, 14
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2023/2023-09-29_WARN-Notice_First-Savings-Bank.pdf?rev=d245687cb0664de68d23dbc4c4c0300f": datetime(
            2023, 11, 30
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2022/2022-10-31_WARN_Booking-com.pdf?rev=4c2c783399a14551897d70117b5ef4e6": datetime(
            2022, 12, 18
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2023/2023-01-06_WARN-Notice_Proper-Group-Holdings-LLC.pdf?rev=a6ed341e4a4241ca89f9c3bfd07b7181": datetime(
            2022, 11, 21
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2023/2023-02-03_WARN-Notice_Marshall-Excelsior.pdf?rev=0919930ebccc4b07b59af8743ceda3e7": datetime(
            2022, 12, 8
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2023/2023-09-05_WARN_Lordstown-Motors-Corp.pdf?rev=0ca41d2a142648ad919337dd63835bad": datetime(
            2023, 11, 4
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2023/2023-01-19_WARN-Notice_Brinks-Home.pdf?rev=e042374bf66e406ea7189ebccd39ddb5": datetime(
            2023, 3, 5
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2022/20220719_WARN-received-Bon-Appetit_Hillsdale-College.pdf?rev=d1d9bdc96963432882758f5c140c07fb": datetime(
            2022, 8, 1
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2023/2023-04-06_WARN_Finlandia.pdf?rev=65b89d07b56d45739981a08e7d2e277e": datetime(
            2023, 3, 3
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2022/2022-03-16_WARN_Assemble-Rite-LTD.pdf?rev=3819d44e254640de836f949d84e52907": datetime(
            2022, 3, 27
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2023/2023-03-31_WARN-Notice_Sandler-Travis-Trade-Advisory-Services.pdf?rev=65f3993f841b4087ba33910365cdc8d7": datetime(
            2023, 5, 31
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2023/2023-09-15_WARN-Notice_Thriveworks.pdf?rev=17ceb50ea2a34937a7313f290bf9d364": datetime(
            2023, 11, 30
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2022/20220509_MPHI---CICT-WARN.pdf?rev=863a6c54bd5c4a7385f2f4324b8d33ee": datetime(
            2022, 7, 1
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2022/202266_MPT-WARN-received.pdf?rev=ef9a5e7decb745988e6fc1a324f8862b": datetime(
            2022, 7, 29
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2022/2022-05-02_FRS_WARN.PDF?rev=d55e644c4f254091a5283713ba97557c": datetime(
            2022, 7, 1
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2022/2022_07-29_WARN_MV-Transportation.pdf?rev=e84e10351c474b50a4883ba0bb6923af": datetime(
            2022, 9, 30
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2022/2022-09-13_WARN_Power-Home-Solar-LLC.pdf?rev=bf1e1f671053408b8ea2863e0e858496": datetime(
            2022, 9, 12
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020b/20200403_Barber_Packaging_WARN.pdf?rev=65104aeac1e64543865dad2ec703138d": datetime(
            2020, 3, 23
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2023/Concentrix-Corporation/2023-01-06_WARN-Notice_Concentrix-Corporation.pdf?rev=b62344a58616421680c203dde26346bb": datetime(
            2023, 3, 4
        ),
        "Beginning July 7, 2025": datetime(2025, 7, 7),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2022/2022-04-06_WARN_Robinson-Industries.pdf?rev=b77dda186c6649da970c30708306c389": datetime(
            2022, 3, 31
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2023/2023-08-02_WARN_Kelsey-Hospital.pdf?rev=031cdf4bb5c943af9614c457bd67cc41": datetime(
            2023, 10, 6
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2022/2022-04-08_Mitsubishi-Chemical---WARN-Letter-to-State.pdf?rev=1f21d92bcf8341a6b0cc3dac145fe4b4": datetime(
            2022, 4, 19
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2023/2023-04-07_WARN_Flint-Genesee-Chamber-of-Commerce.pdf?rev=68a43bcc0e8c48c8bdd6bab00bbeafaf": datetime(
            2023, 5, 29
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2022/2022-08-01_WARN_GEO-Secure-Services_North-Lake-Correctional-Facility.pdf?rev=e4fb2daeb3e84604ac90739ca48123ef": datetime(
            2022, 9, 30
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2023/Eagle-Industries-Inc/2023-09-21_WARN-Notice_Eagle-Industries-Inc_Updated.pdf?rev=f56a849c430142f6b6aef769d3b06887": None,
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2022/2022-03-09_WARN_PAE.pdf?rev=f0bd9f292d6f4bd3a9df586e372ad90b": datetime(
            2022, 2, 1
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2023/2023-08-15_WARN_AH.pdf?rev=262eb8122be04eb28099fa9f455e0017": datetime(
            2023, 10, 14
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2022/2022-11-17_WARN_Home-Point-Financial-Corp.pdf?rev=1bb21c4ecd274ef4a97f3a042586ecae": datetime(
            2022, 11, 17
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2022/2022-10-21_WARN_DHL.pdf?rev=5516ce3f7528425aa9bc1864e0b6e62f": datetime(
            2022, 11, 12
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2023/2023-09-15_WARN_CIE-NEWCOR.pdf?rev=5b0dfe476fb54a3a9422f2f24fc68c24": datetime(
            2023, 10, 2
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2023/2023-08-04_WARN_Minnie-Marie-Bakers.pdf?rev=1240bd0d3bd94862a7e4c8a7ccd44e19": datetime(
            2023, 9, 30
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2022/2022-11-10_WARN_Wayne-Metropolitan-Community.pdf?rev=a67f5339cefa42628a626cb461fc7fbf": datetime(
            2022, 12, 30
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2023/2023-05-19_WARN_Lordstown-Motors-Corp.pdf?rev=057b22a8c62041b6967c70473d6c88ac": datetime(
            2023, 7, 17
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2023/2023-04-11_WARN_Homepoint.pdf?rev=c2326382c7f5419c8b7d2849997f3116": datetime(
            2023, 4, 11
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2023/2023-06-20_WARN_Autism-Home-Support-Services-LLC.pdf?rev=aba6397774e5462db56859c74e6c7981": datetime(
            2023, 8, 21
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2023/2023-09-27_WARN-Notice_Cascades.pdf?rev=bedfcc6954ea4b6cb90d75ba5472ba2f": datetime(
            2023, 9, 22
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2023/2023-05-01_WARN_Lear-Corporation_Nevada-Plant.pdf?rev=6729f04ca3e34d198b7b173ff2ef304b": datetime(
            2023, 6, 30
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2023/2023-01-11_WARN-Notice_Clover-Imaging-Group.pdf?rev=001955f6c37a47919563c507ef08a68e": datetime(
            2023, 3, 14
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2023/2023-05-31_WARN_Illinois-Tool-Works-Inc.pdf?rev=a8805624debd459494df563cacb40abb": datetime(
            2023, 5, 30
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2022/2022-03-24_WARN_Pretium-Packaging-LLC.pdf?rev=971ea10ae2eb456bbe9af64fa63bf101": datetime(
            2022, 3, 11
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2022/Armor-Express-Notice_MICH-DLEO.pdf?rev=819cbe83a273482ca9d080f18203bde8": datetime(
            2022, 1, 5
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020/WARN_-_Allied_Universal_Security_Services.pdf?rev=43e8a57c60d44bdf9a6b053f2d81dc57": datetime(
            2021, 1, 31
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2023/2023-06-16_WARN_Quality-Spring-Togo.pdf?rev=6b25b70fdc8a47218683ce6100c480a2": datetime(
            2023, 8, 1
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2022/2022-09-21_WARN_Dunn-Paper-Inc_DP-Holdings-LLC.pdf?rev=e7ce9267bcd2430c869df8129a0f1905": datetime(
            2022, 11, 18
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2023/2023-08-02_WARN_Yellow-Corp.pdf?rev=3f63ad4092fa4ff193903bbda3dd3388": datetime(
            2023, 7, 24
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2022/2022-06-20_Sturgis-Hospital_State-dislocated-worker-unit.pdf?rev=241a4defebf144539913171959f56bd6": datetime(
            2022, 7, 22
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2023/2023-01-31_WARN-Notice_Faurecia-Highland-Park.pdf?rev=428df8b8dc414ef4916e2c9464e1af82": datetime(
            2023, 2, 20
        ),
        "Beginning January 31, 2025": datetime(2025, 1, 31),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2023/2023-07-21_WARN_Notice_Faurecia---Highland-Park-JIT.pdf?rev=f0415bab66e04ba1b28574190c066bc4": datetime(
            2023, 9, 23
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2022/20220519Warn-Notice--Penske-Romulus.pdf?rev=756f912dbee34354b0cbda7fa7702456": datetime(
            2022, 7, 18
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2022/2022-02-01_WARN_LearCorp.pdf?rev=3bc2db4074274b96b10659ce8a855ec8": datetime(
            2022, 3, 31
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2022/2022-03-22_WARN-_Sodexo_Alma.pdf?rev=da622a645df543e5b039ad2842e9dd9f": datetime(
            2022, 6, 30
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2022/20220601_WARN_Dynamic-BDC.pdf?rev=462962d015a74316889b0a0c5216c81c": datetime(
            2022, 7, 31
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2023/2023-03-22_WARN-Notice_Yellow-Corporation.pdf?rev=8747814111454fa0baf22ae22a274bb4": datetime(
            2023, 5, 28
        ),
        "April 31, 2019": None,
        "https://www.michigan.gov/documents/leo/2020-04-10_Agrati_Inc._-_WARN_686778_7.pdf": None,
        "https://www.michigan.gov/documents/leo/2020-06-29_Normal_Michigan_Inc._Regional_Headquarters_WARN_695247_7.pdf": None,
        "https://www.michigan.gov/documents/leo/YMCA_of_Greater_Grand_Rapids_-_WARN_Notification_7.27.20_signed_697533_7.pdf": None,
        "https://www.michigan.gov/documents/leo/2020-06-15_US_Steel_Corp._Great_Lakes_Works-combined_693841_7.pdf": None,
        "https://www.michigan.gov/documents/leo/2020.04.15_The_Tile_Company_Layoffs_Permanent_WARN_Notice_687530_7.pdf": None,
        "https://www.michigan.gov/documents/leo/2020-06-08_Creative_Dining_Services_Inc._WARN_693217_7.pdf": None,
        "https://www.michigan.gov/documents/leo/2020-04-07_Eagle_Industries_Inc._WARN_686217_7.pdf": None,
        "https://www.michigan.gov/documents/leo/Paradies_Lagardere.2_-_WARN_Notice_696956_7.pdf": None,
        "https://www.michigan.gov/documents/leo/2020-04-07_L.O._Eye_Care_WARN_686225_7.pdf": None,
        "https://www.michigan.gov/documents/leo/2020.04.15_The_Tile_Company_Temp_Layoff_WARN_Notice_687531_7.pdf": None,
        "https://www.michigan.gov/documents/leo/2020-04-13_Samsung_SDI_America_Inc._WARN_687009_7.pdf": None,
        "https://www.michigan.gov/documents/leo/2020-04-13_Yazaki_North_America_Inc.-WARN_687020_7.pdf": None,
        "https://www.michigan.gov/documents/leo/2020-05-18_Gill_Industries_Inc._Plainfield_WARN_691001_7.pdf": None,
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020b/20200730_Spirit_WARN_Notice.pdf?rev=d4225ac67e144dfea9434518c976ac35": datetime(
            2020, 10, 1
        ),
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2025/2025-12-15_WARN-Notice_C3-Industries-Inc.pdf?rev=2124411748d9487ab84dbb26a2d19947": datetime(
            2026, 2, 14
        ),
        "December 5, 2025, and January 16, 2026": datetime(2025, 12, 5),
        "December 5, 2025; January 16, 2026; and March 20, 2026": datetime(2025, 12, 5),
    }
    jobs_corrections = {
        "80*": 80,
        "Unreported": None,
        "1 remote Michigan worker": 1,
        "138 (133 Zeeland, 5 Traverse City)": 138,
        "2 remote workers": 2,
        "12 remote workers": 12,
        "3 remote Michigan workers": 3,
        "Approximately 25": 25,
        "Approximately 156": 156,
        "Approximately 95": 95,
        "1 Michigan remote worker": 1,
        "6 impacted Michigan workers": 6,
        "1 Michigan remote worker": 1,
        "132 (approximately)": 132,
        "2,458": 2458,
        "1 remote worker": 1,
        "2,453": 2453,
        "18 Michigan remote workers": 18,
        "2 Michigan remote workers": 2,
        "1,215": 2,
        "Unknown": None,
        "163, 204, 130, 191": 163,
        "2,000": 2000,
        "1,295": 1295,
        "1,298": 1298,
        "1,318": 1318,
        "1,012": 1012,
        "1,286": 1286,
        "2,900": 2900,
        "2,289": 2289,
        "1,656": 1656,
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020b/20200409_Precision_Vehicle_Solutions_WARN.pdf?rev=a7d1de1a6ce74471b6bd7d0335d4fb1b": 180,
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020/2020-12-15_Updated_RustyBucket_WARN.pdf?rev=0b6c40673ef344d8811075dad1703b1d": 74,
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020c/2020-08-24_Vetta_LLC_WARN.pdf?rev=0300f2738e514ac5a2f12c87fbff26f3": 73,
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020b/20200604_Marriott_Hotel_Services_WARN.pdf?rev=1ebedde528234cbeac7e2610f8521dc2": 134,
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020b/20200409_Hooters_WARN.pdf?rev=74b227f87fbe42e18fd91eb91591c72d": 87,
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020/2020-10-07_LansingEntertain_WARN.pdf?rev=e38d1d2729174751bc59da437085687f": None,
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020c/2020-09-18_PF_Changs_China_Bistro_WARN_Notice.pdf?rev=43f467ed95bb41eba26d275471056588": 600,
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020b/Hertz_updated_WARN_Notice_5232020.pdf?rev=24ae228763964777aa21756b7610bdc1": 107,
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020b/20200622_SwissportGerald_R_Ford_International_Airport_WARN.pdf?rev=06218d866b8c425399d825b436e40595": 55,
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2021/2021_01-08_UAW_Chrysler_WARN.pdf?rev=675c529eb9744dbd84b5dbf0dbfc473c": 97,
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020b/20200716_3rdUpdated_IAC_Alma_WARN.pdf?rev=a26a934f69a2411ebe88b16e27d61829": 39,
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2021/2021-06-07_Progenity_WARN.pdf?rev=afc8e375123e42b9aab9b66779a3db40": 110,
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020/20200424_Schafer_Woodworks_WARN.pdf?rev=5523b6e3e6a249ee97bfe59496b4c5aa": 20,  # ish
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020b/20200730_Spirit_WARN_Notice.pdf?rev=d4225ac67e144dfea9434518c976ac35": 190,
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020/2020-11-19_MGM_Grand_Detroit_WARN.pdf?rev=8f6aaf7a01834b298f2df036b5909a21": 1561,
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020b/20200409_ProspectWARN.pdf?rev=410a938ee47d42d992125301b4ec9ad3": 132,
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2023/Davids-Bridal/2023-06-29_WARN_Davids_Bridal.pdf?rev=3ca5f1125826490eb4e5fc156acf661f": None,
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020b/20200413_Four_Winds_Casinos_WARN.pdf?rev=4f85faa7faf64383bdec07461980ee41": 1489,
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020b/20200602_Westin_Detroit_Metro_Airport_WARN_Notice.pdf?rev=d6681916f045487a9887f709c9dafe3c": 197,
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020/2020-07-20_MotorCity_Casino_Hotel_WARN.pdf?rev=d4dc8ded496248eebb01fbc226293eea": None,  # Many, but attachment not in PDF
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020b/20200604_Westin_Book_Caddillac_WARN.pdf?rev=4b08e40a021f444e97432f296cbb4b83": 227,
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020/20200520_Townsend_Hotel_WARN.pdf?rev=afcf5ccc7de54350996bfb9bdddba0df": 60,
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020/20200512_Marriott_Detroit_Livonia_WARN.pdf?rev=4de1917eb90c409fa6a588aa7227bf64": None,  # Many, no attachment
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020c/20200616_Jacobsen_Daniels_WARN_Notice.pdf?rev=58027249107a43ea9ec99918b7967c98": 7,
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020/20200424_Punch_Bowl_Social_WARN.pdf?rev=1e2e11298d6b4c81b86580300a86ba13": 97,
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020/20200420_Tilden_Mining_WARN.pdf?rev=6344a21d47d74208b0bffe141ec3b6ca": 687,
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020/Walbro_LLC__WARN_Notice_20200526.pdf?rev=f00602a0acd24b23ad6b472133473813": None,  # No attachment
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020/20200415_Wolverine_Corporation_WARN.pdf?rev=bea449562bf74a489ffd88ddd89d0d8f": 70,
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020c/20200709_TownePlace_WARN_Notice.pdf?rev=822b4ac3a2d9482d9d0fab825a56b0b6": 14,
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020b/20200723_MotorCity_Casino_Hotel_WARN.pdf?rev=87c44b485e0b4fb580d78947438bf5b6": 2554,
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020b/20200618_Staples_WARN_Notice.pdf?rev=5ced945de3c24dd9969524b776a78750": 61,
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020c/2020-09-17_Tennaco_WARN.pdf?rev=e36528ccfe13487eb5e9c8b82b894fc9": 121,
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020b/20200601_Wireless_Vision_WARN.pdf?rev=5e66806e04b0428baeba7d8f9fdcc8f4": 37,
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020b/20200408_Pace_Industrices_WARN.pdf?rev=b2a38964abc344eaa1b8d5e1beff0b22": 456,
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020/20200420_Marsh_Plating_WARN.pdf?rev=754d8a1a3dcb4337a2735cb926521f4d": 59,
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020c/2020-11-24_MotorCity_Casino_WARN.pdf?rev=04de99f317824c8696aaa7627a9efb45": None,  # Many, but no counts of positions
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020/20200505_MGM_Grand_WARN.pdf?rev=ff136f59e59b47e287ed6354ad6a9076": 2632,
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020/2020-12-05_Tech_Mahindra_WARN.pdf?rev=b8f9eb6d6d8340938780c83296b3f1bc": 81,
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020c/20200709_Hilton_Garden_Inn_WARN_Notice.pdf?rev=5e94c1549c794842a2fb30c17be8f55e": 39,
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020/2020-12-21_NBHX_Trim_USA_WARN.pdf?rev=17ba9d4f9cb347de898c758c72000b08": 76,
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020b/20200616_JacobsenDaniels_WARN_Notice.pdf?rev=96fdd5f611b24316b1236751b3dda772": 24,
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020/2020_WARN_Notice_State_V2.pdf?rev=e5640aaf018944f1846ac0420b83ebe6": 50,
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020/20200430_Hertz_WARN.pdf?rev=e4d1304ab6d949ef8a923bc1de815712": 106,
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020/2020-09-30_Kroger_WARN.pdf?rev=0e5d4200b97946a9bec77381233a0fc2": 73,  # 73 in union. No attachment. No non-union listing.
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020/20200522_Marriott_Auburn_Hills_Pontiac_WARN.pdf?rev=a26034c66f5a4bf182b330817c9a5d63": 101,
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020/20200420_Williams_Intl_WARN.pdf?rev=7508e61f18ea42fea38bd745284287e2": 248,
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020b/20200409_Morbark_WARN.pdf?rev=95e72c91fb6a4f3fa59a04c837a40c24": 182,
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020/2020-09-03_Greektown_Casino-Hotel_WARN.pdf?rev=69f46393da7d4ee18ca8364cebb20935": 43,  # 43 union; non-union not listed, no attachment.
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020b/20200707_Updated_Spire_WARN.pdf?rev=6857a98b59e34c269d567657b00cd9e9": 159,
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020/20200423_Visionworks_WARN.pdf?rev=5fefb05a4a1a44c58a927465ed43eacc": None,  # No attachment
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020/2020-08-17_HMSHost_WARN_no_names.pdf?rev=677f45d598ee483ba69b4842dcdf6e5d": None,  # No count, no attachment
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020/20200506_Great_Lakes_Specialty_Finance_WARN.pdf?rev=c8342ca76f3f474faf5d17320e8bd0c5": 62,
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020b/20200720_Leadec_WARN.pdf?rev=6b62fff17bf6480bbd9ea1177ab2bdf6": 50,
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020/20200518_Grand_River_Polishing_WARN.pdf?rev=2e28eaa7cfdd48cea05b018b475f3437": 20,
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2021/2021-03-08_WARN_JDNormanIndustries.pdf?rev=a00f3dadc0a9434db1ea76d4c4cd09bc": 56,
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020b/20200709_Holiday_Inn_GR_WARN_Notice.pdf?rev=4b1829c8c5a241bf96cdd3074c6e7809": 36,
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020/2020-09-02_WARN_-_Orlans_PC.pdf?rev=d7ceffa7bd9d4adb9926930530d9df54": 60,
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020c/20200811_Sky_Chefs_DTW_WARN_Notice.pdf?rev=74236f79de634cb3ae4221a53c756417": 102,
        "https://www.michigan.gov/leo/-/media/Project/Websites/leo/Documents/WD-DATA_PUBLIC_WARN_NOTICES4/2020/2020-09-24_SP_Plus_Corp_WARN_Notice.pdf?rev=b304f366d9924cc58330b6182da808ca": 95,
        "https://www.michigan.gov/documents/leo/2020-06-15_US_Steel_Corp._Great_Lakes_Works-combined_693841_7.pdf": None,
        "https://www.michigan.gov/documents/leo/2020-04-07_L.O._Eye_Care_WARN_686225_7.pdf": None,
        "https://www.michigan.gov/documents/leo/YMCA_of_Greater_Grand_Rapids_-_WARN_Notification_7.27.20_signed_697533_7.pdf": None,
        "https://www.michigan.gov/documents/leo/Paradies_Lagardere.2_-_WARN_Notice_696956_7.pdf": None,
        "https://www.michigan.gov/documents/leo/2020-06-29_Normal_Michigan_Inc._Regional_Headquarters_WARN_695247_7.pdf": None,
        "https://www.michigan.gov/documents/leo/2020.04.15_The_Tile_Company_Temp_Layoff_WARN_Notice_687531_7.pdf": None,
        "https://www.michigan.gov/documents/leo/2020-04-13_Yazaki_North_America_Inc.-WARN_687020_7.pdf": None,
        "https://www.michigan.gov/documents/leo/2020-04-13_Samsung_SDI_America_Inc._WARN_687009_7.pdf": None,
        "https://www.michigan.gov/documents/leo/2020.04.15_The_Tile_Company_Layoffs_Permanent_WARN_Notice_687530_7.pdf": None,
        "138 (133 Zeeland 5 Traverse City)": 138,
        "163 204 130 191": 688,
    }

    def check_if_closure(self, row: typing.Dict) -> typing.Optional[bool]:
        """Determine whether a row is a closure or not.

        Args:
            row (dict): The raw row of data.

        Returns: A boolean or null
        """
        return "clos" in row["action"].lower() or None
