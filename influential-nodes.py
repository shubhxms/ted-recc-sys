# -*- coding: utf-8 -*-
"""Untitled1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1u4tUHsazKoE90amrtmaVUnlxL0Q7-K61
"""

import csv
import ast

def memoize(f):
    memo = {}
    def helper(node, length, graph):
        graph_id = id(graph)
        if (node, length, graph_id) not in memo:
            memo[(node, length, graph_id)] = f(node, length, graph)
        return memo[(node, length, graph_id)]
    return helper

def get_related_talks(talk):
    related_talks_str = talk[1]
    related_talks_list = ast.literal_eval(related_talks_str)
    return [talk_dict['id'] for talk_dict in related_talks_list]

def get_cycles_helper(node, length, visited, path, cycles, graph):
    if length == 0:
        if node in graph[path[0]]:
            cycle = tuple(path + [node])
            cycles.add(cycle)
    else:
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                get_cycles_helper(neighbor, length-1, visited.copy(), path+[node], cycles, graph)
        visited.remove(node)

@memoize
def get_cycles(node, length, graph):
    cycles = set()
    visited = set()
    get_cycles_helper(node, length, visited, [], cycles, graph)
    return cycles
    
def get_influential_nodes(graph):
    cycles = set()
    for node in graph:
        for length in range(4, 11):
            try:
                cycles.update(get_cycles(node, length, graph))
            except KeyError:
                pass
    node_counts = {}
    for cycle in cycles:
        for node in cycle:
            if node in node_counts:
                node_counts[node] += 1
            else:
                node_counts[node] = 1
    influential_nodes = [node for node in node_counts if node_counts[node] > 1]
    return influential_nodes

with open('/content/ted_talks.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    next(csv_reader)  # skip header row
    graph = {}
    for row in csv_reader:
        talk_id = row[0]
        related_talks = get_related_talks(row)
        graph[talk_id] = related_talks
    influential_nodes = get_influential_nodes(graph)
    print("Influential nodes:", influential_nodes)

""">### output
`Influential nodes: ['2096', '2555', '2145', '1181', '2133', '14', '1571', '606', '144', '32', '871', '1371', '955', '874', '640', '187', '45086', '20919', '2498', '2467', '3231', '472', '1966', '1559', '1015', '2129', '2078', '2753', '1044', '2783', '41105', '2768', '1810', '3686', '50755', '56535', '64549', '49429', '52811', '62406', '54352', '58017', '63775', '2570', '35766', '2354', '39689', '30303', '2546', '3593', '476', '475', '409', '993', '790', '2389', '24509', '2003', '2586', '2276', '36415', '32412', '46386', '63242', '60742', '2522', '46536', '5072', '60063', '23058', '58104', '2052', '1322', '492', '1402', '1195', '1260', '176', '2593', '1082', '2821', '2599', '1343', '859', '910', '13778', '765', '10', '263', '348', '2183', '31', '174', '359', '219', '20259', '2453', '2831', '38079', '12060', '1378', '2303', '1229', '1787', '1397', '1320', '12', '2109', '2680', '1605', '437', '331', '227', '6', '138', '1526', '1105', '631', '218', '103', '560', '405', '19', '1131', '38', '2114', '79', '91', '127', '151', '2113', '873', '973', '1373', '590', '431', '266', '207', '372', '17923', '1433', '1147', '231', '49', '2375', '2504', '50586', '26920', '1199', '399', '178', '42247', '2550', '2476', '2235', '1854', '1846', '183', '35', '13', '750', '761', '1047', '888', '2273', '2242', '179', '1156', '110', '22799', '19893', '805', '117', '1757', '1288', '2247', '9214', '1472', '60310', '1600', '2136', '392', '43', '122', '646', '1464', '24', '786', '2147', '667', '634', '23942', '24076', '1340', '1749', '104', '3280', '355', '1070', '26073', '23823', '23886', '24486', '20317', '29668', '23777', '318', '2128', '551', '421', '141', '2429', '2342', '49129', '967', '1879', '43932', '2471', '59801', '9473', '2245', '24019', '28863', '31122', '41452', '39512', '1051', '986', '2756', '49732', '1239', '804', '2869', '679', '1216', '130', '677', '674', '30300', '12501', '2316', '50956', '1160', '2299', '13247', '52195', '52466', '2130', '43200', '2171', '2005', '2635', '2370', '1509', '798', '24012', '23880', '1426', '23716', '1564', '33801', '660', '2610', '2351', '1177', '23931', '24136', '24254', '24343', '23740', '673', '647', '676', '1074', '965', '2357', '1200', '206', '830', '467', '264', '343', '40', '614', '1470', '702', '613', '2', '1227', '1144', '1579', '1461', '346', '549', '2278', '1909', '32269', '15813', '2685', '1761', '16', '2590', '2146', '14614', '4755', '2311', '2095', '49131', '36479', '20368', '2841', '2645', '1291', '246', '286', '28953', '883', '648', '920', '1210', '1976', '2260', '922', '744', '1845', '1562', '1626', '142', '2220', '53', '1429', '2107', '2310', '773', '1531', '1913', '2050', '1710', '1487', '2100', '1446', '46', '1298', '1985', '2286', '2158', '23979', '49002', '29391', '2595', '23117', '1826', '1443', '1878', '63241', '46532', '1360', '1981', '939', '791', '518', '502', '89', '1631', '36760', '2875', '1306', '2039', '147', '253', '27790', '2654', '251', '247', '216', '274', '63', '1492', '24035', '27221', '23894', '33931', '280', '571', '2014', '195', '165', '996', '361', '146', '936', '1432', '1213', '168', '69', '11', '2307', '315', '1677', '657', '2682', '2636', '2839', '2609', '50959', '1187', '23972', '1124', '1935', '408', '2340', '1498', '1624', '6671', '2057', '23422', '23877', '1163', '428', '2238', '55546', '1352', '193', '192', '74', '197', '396', '1347', '28', '2227', '2545', '2656', '2468', '2029', '1480', '1286', '2677', '46456', '2131', '1994', '1500', '32035', '31235', '32389', '30821', '29063', '321', '198', '1811', '909', '1862', '31821', '1083', '154', '156', '330', '55342', '1760', '1524', '785', '1476', '1033', '53059', '2732', '1040', '1943', '214', '2670', '24392', '23423', '3671', '2898', '55993', '23936', '729', '2878', '2532', '2717', '2538', '639', '158', '169', '2684', '1809', '11226', '938', '628', '46577', '3136', '436', '489', '182', '172', '1977', '46526', '17733', '998', '322', '1173', '1440', '1465', '1280', '468', '1140', '37225', '24044', '416', '2249', '1822', '23847', '18512', '2817', '1794', '33799', '23862', '35386', '2767', '24209', '59862', '329', '447', '1808', '23736', '20101', '23714', '1386', '242', '1409', '1050', '1709', '10376', '1997', '1830', '5351', '2889', '601', '57639', '47', '701', '404', '20753', '2237', '23865', '2424', '2088', '2166', '50574', '45233', '55', '800', '21925', '1002', '233', '1034', '1232', '2491', '52752', '52061', '23927', '56860', '10190', '2874', '57924', '2466', '469', '41224', '1882', '1103', '1645', '836', '58601', '2289', '1696', '23794', '53671', '503', '1926', '1850', '56811', '24091', '24006', '13567', '24017', '850', '833', '80', '323', '814', '28438', '28518', '3585', '37800', '1738', '2526', '1728', '66', '2103', '520', '8955', '2568', '2294', '1986', '2426', '65', '40636', '685', '1705', '32190', '2410', '1813', '1671', '1450', '1385', '2557', '1146', '23479', '40714', '21977', '17698', '50986', '46592', '24453', '40769', '27674', '260', '24133', '2764', '57701', '2301', '1185', '821', '675', '815', '2588', '1687', '887', '2582', '1538', '1530', '1685', '21701', '27750', '2743', '1410', '57918', '1011', '155', '232', '59', '31121', '45', '1684', '1372', '926', '54', '494', '157', '185', '270', '799', '1278', '24350', '55061', '1501', '48847', '3013', '13062', '39941', '556', '2127', '159', '49735', '1718', '24284', '2214', '1906', '1030', '2866', '2614', '2314', '62791', '1861', '24113', '17994', '23913', '1020', '1184', '1565', '832', '1851', '152', '13517', '46585', '31240', '27692', '2283', '769', '2017', '482', '1285', '443', '49136', '1127', '175', '1678', '145', '1995', '140', '121', '123', '36', '995', '2790', '1522', '57604', '2765', '2160', '41764', '29009', '54358', '2517', '1141', '297', '324', '24339', '23889', '23827', '2750', '28418', '24488', '41652', '470', '126', '2116', '77', '8', '26263', '1139', '40280', '1095', '1182', '1865', '1843', '2007', '816', '1618', '20721', '44373', '45407', '18514', '2309', '22704', '2607', '1623', '501', '435', '1474', '8421', '2118', '2675', '2230', '5116', '54125', '62790', '2132', '60819', '39503', '55319', '64548', '45969', '2110', '2449', '24354', '960', '860', '1018', '2099', '1339', '2547', '6496', '9687', '2493', '2529', '1053', '422', '1894', '1167', '58787', '49931', '36215', '27219', '23986', '1376', '2346', '1577', '1750', '52467', '42604', '2201', '1698', '23806', '2749', '2320', '2736', '2723', '1984', '1781', '683', '51', '862', '940', '1394', '885', '1201', '581', '478', '663', '755', '651', '538', '2648', '2603', '2624', '19172', '44372', '194', '1853', '2396', '371', '1946', '1172', '115', '22703', '6639', '2708', '24111', '19831', '24286', '319', '2061', '1581', '362', '1734', '1655', '1359', '1575', '1231', '1922', '2243', '2689', '3633', '2592', '131', '872', '230', '3362', '2891', '2462', '6669', '2881', '48103', '50', '2106', '1820', '1221', '1950', '5451', '24283', '2244', '24026', '2886', '2439', '863', '300', '162', '957', '1149', '17713', '17711', '17712', '17699', '1331', '789', '1109', '1724', '2291', '63622', '2329', '1444', '783', '306', '43862', '1256', '21930', '2616', '1965', '1667', '36762', '36416', '2659', '2615', '2646', '2120', '1732', '42700', '1644', '2062', '356', '6477', '2711', '580', '1652', '406', '1304', '51538', '948', '36770', '44494', '629', '23958', '2165', '2694', '403', '205', '2251', '1088', '1649', '202', '23896', '21976', '19740', '879', '24405', '1699', '41226', '49435', '19330', '1006', '852', '1668', '1543', '1916', '1495', '1969', '1604', '547', '1837', '1927', '929', '249', '24922', '23713', '2076', '723', '4', '1711', '1475', '9296', '19478', '161', '2022', '1803', '1106', '23938', '52468', '1302', '258', '976', '18', '23416', '589', '1674', '48627', '8788', '2418', '64354', '2436', '2124', '33565', '1628', '19460', '2579', '35563', '1056', '28172', '2402', '1284', '54863', '2713', '2890', '2572', '2558', '51070', '2739', '52490', '52395', '27953', '1114', '386', '1650', '18592', '53667', '1785', '1356', '752', '2384', '2731', '2721', '1096', '2031', '325', '328', '24167', '1178', '189', '2356', '964', '5', '1354', '1311', '968', '1999', '2008', '5392', '2724', '2500', '188', '186', '102', '2045', '1186', '229', '125', '36659', '2433', '1947', '3328', '13465', '1873', '797', '540', '143', '818', '41873', '61611', '35897', '26676', '30207', '21700', '1357', '49356', '31375', '1956', '481', '50982', '76', '340', '21191', '61317', '46581', '44216', '45972', '19535', '1325', '39220', '2055', '1791', '2101', '1253', '523', '190', '439', '1361', '1770', '1944', '1752', '1782', '1619', '1113', '2033', '2484', '1308', '24504', '2077', '23735', '41223', '24278', '1148', '1016', '82', '819', '1251', '31236', '54513', '46518', '849', '2345', '1089', '23920', '20779', '1271', '24357', '2046', '4366', '25241', '853', '1819', '1445', '50638', '6672', '1940', '2507', '429', '41038', '856', '222', '148', '374', '86', '1920', '1207', '1838', '58018', '2661', '2330', '1925', '24306', '307', '42', '2092', '490', '24257', '644', '46453', '46528', '250', '1379', '18011', '52190', '2775', '40410', '24331', '2755', '28070', '1423', '2063', '1651', '592', '84', '650', '1039', '23788', '24227', '23929', '23758', '24328', '932', '1817', '1121', '1928', '5990', '55544', '24266', '24140', '24273', '24180', '2740', '42488', '1393', '18517', '2797', '30988', '2417', '1657', '1570', '1007', '855', '23583', '1058', '2170', '820', '418', '2745', '23785', '21650', '49279', '17848', '1891', '1832', '1744', '1399', '1847', '13464', '53235', '1324', '2583', '881', '598', '1727', '911', '50990', '50576', '2075', '1788', '412', '1152', '516', '129', '245', '1630', '24249', '53276', '49114', '2412', '2241', '41353', '9987', '24420', '1576', '1194', '916', '24275', '60479', '24268', '53297', '1936', '326', '18928', '213', '914', '1295', '24269', '962', '445', '499', '963', '9982', '2366', '557', '63294', '30180', '23420', '30813', '259', '684', '3', '584', '951', '1196', '2860', '42089', '64437', '24558', '9403', '19266', '27105', '1552', '621', '64173', '20757', '952', '1108', '1206', '474', '2054', '8588', '1912', '28544', '25340', '25132', '51452', '32414', '1396', '1910', '2349', '31863', '45868', '1267', '9984', '1471', '18774', '2653', '2560', '2427', '1617', '983', '1971', '1959', '2882', '57144', '3616', '25751', '37758', '26075', '46590', '24262', '6019', '2601', '2549', '672', '1204', '1503', '36284', '33800', '1815', '1197', '898', '1723', '18469', '6234', '2710', '1297', '1168', '24178', '20692', '19727', '37661', '24119', '24095', '23813', '23976', '23801', '2352', '43407', '1488', '30527', '3364', '2282', '31459', '28542', '36684', '23850', '22979', '2210', '537', '1733', '390', '1037', '1755', '2180', '2382', '14471', '710', '919', '719', '545', '689', '8786', '1457', '335', '19173', '6286', '46591', '31857', '27696', '25090', '763', '1191', '1473', '1078', '26010', '108', '981', '1898', '87', '50657', '57260', '46589', '49424', '1806', '1669', '27632', '25874', '49779', '24303', '1942', '3590', '2373', '44200', '24432', '9507', '2651', '1549', '1072', '20008', '19851', '38072', '40540', '12498', '10360', '10681', '24382', '2759', '24232', '2776', '886', '1758', '2825', '2690', '57418', '83', '252', '39', '31810', '41570', '24064', '24024', '2281', '3613', '959', '364', '1700', '2672', '1093', '54750', '8418', '1974', '1036', '1675', '1032', '1499', '1434', '1085', '1634', '1353', '56', '2448', '2115', '1827', '2020', '1485', '1592', '9986', '2323', '587', '1413', '603', '40949', '2761', '1337', '2541', '1171', '2511', '1237', '1218', '236', '320', '57908', '3587', '2455', '5139', '1938', '1911', '59145', '2495', '23933', '6857', '2313', '50793', '265', '1458', '544', '554', '2105', '2285', '509', '37137', '2833', '21150', '15290', '24471', '1945', '23800', '23844', '1117', '70', '1384', '1335', '2026', '2388', '2216', '38073', '2758', '20319', '24003', '2747', '49440', '24041', '29459', '931', '60021', '2252', '75', '13878', '24387', '1468', '35352', '33778', '1489', '780', '12803', '1001', '912', '1455', '974', '620', '24414', '1066', '2073', '1520', '1098', '60835', '2518', '622', '12727', '17849', '670', '2620', '60390', '2483', '31441', '10835', '23965', '2494', '826', '1949', '870', '510', '2505', '48275', '55593', '40035', '36771', '63786', '36214', '388', '713', '2662', '2024', '1136', '56434', '655', '2551', '63363', '51634', '22752', '215', '1751', '2213', '171', '1003', '1112', '1046', '50640', '2531', '21895', '29411', '1481', '2742', '2778', '35607', '1165', '1825', '1534', '1639', '20085', '2246', '2065', '994', '594', '23811', '24021', '62866', '978', '718', '60184', '1643', '1683', '896', '1242', '2844', '2752', '56901', '1133', '901', '23480', '23799', '2709', '2692', '23971', '42821', '2163', '2013', '2411', '1398', '1100', '23891', '55275', '24455', '3612', '59157', '62347', '1672', '2175', '2152', '1666', '1403', '2434', '2871', '2528', '866', '2642', '58016', '1369', '1756', '2883', '1358', '2413', '1842', '2423', '2470', '44204', '29523', '353', '2028', '1451', '1532', '1886', '2315', '10362', '2771', '1866', '53587', '2824', '2443', '484', '1535', '1289', '727', '40753', '1601', '2848', '31812', '1091', '714', '1268', '1244', '339', '29769', '802', '57479', '26074', '524', '23887', '40201', '8422', '64360', '24238', '17238', '298', '36385', '695', '92', '23977', '18818', '2757', '2250', '21804', '22701', '2265', '1075', '3623', '1512', '1505', '53523', '26076', '48272', '1060', '1585', '1421', '748', '2361', '1731', '1739', '3592', '46593', '23738', '25339', '53522', '23879', '659', '1247', '23483', '2393', '2808', '2707', '2223', '52397', '52268', '1690', '1777', '1090', '54353', '23995', '1921', '1627', '56527', '652', '46522', '2801', '2482', '2091', '12351', '12349', '12348', '12347', '10193', '1895', '50803', '52402', '602', '1518', '715', '1892', '12571', '1205', '21039', '36063', '10378', '2358', '2683', '23783', '24205', '2479', '2001', '555', '32673', '33930', '12346', '2591', '2487', '1824', '15398', '1954', '1767', '842', '704', '734', '1142', '1296', '2344', '52269', '971', '37986', '2419', '18219', '2696', '1816', '72', '118', '52073', '52463', '1459', '1281', '1620', '1118', '625', '696', '1054', '51605', '23928', '891', '414', '1784', '712', '60135', '51996', '2548', '2787', '2781', '2606', '2533', '40709', '2414', '471', '1282', '2228', '2720', '41656', '42546', '42248', '1506', '1264', '1478', '2016', '706', '1580', '1126', '24324', '53089', '17851', '53024', '26916', '9988', '23724', '775', '1918', '55113', '31700', '1766', '1250', '1107', '531', '1563', '2072', '1508', '2519', '1907', '19092', '1555', '1656', '1855', '892', '809', '949', '865', '9951', '36811', '626', '1129', '30820', '1490', '114', '2049', '662', '2288', '1608', '1848', '6018', '466', '1660', '379', '558', '38719', '1901', '2272', '1496', '1370', '1158', '504', '62085', '1299', '40635', '29265', '10038', '8419', '2501', '19174', '2279', '2657', '30507', '1223', '10363', '698', '27', '10622', '2704', '17697', '21033', '1689', '724', '50058', '1528', '899', '23968', '1363', '1408', '14485', '56009', '49398', '637', '24457', '2404', '44823', '8780', '1908', '570', '97', '1527', '2849', '29160', '2143', '35903', '24045', '2071', '1835', '52062', '1952', '33924', '843', '60315', '2255', '2798', '2515', '2374', '1342', '2472', '2879', '1122', '1588', '2430', '1364', '37985', '402', '1346', '1547', '1765', '1960', '1595', '181', '627', '1101', '1764', '1111', '24356', '15457', '31779', '29159', '1703', '1610', '716', '164', '276', '1154', '1839', '1636', '1214', '1317', '1929', '13014', '2617', '241', '2576', '13035', '1963', '1419', '1387', '57', '36404', '1349', '1000', '2854', '2885', '20089', '49358', '20044', '2870', '19995', '2792', '1762', '61575', '29998', '4958', '6594', '1596', '24109', '2506', '45045', '5458', '423', '41', '23912', '24399', '24049', '433', '9', '1704', '512', '1174', '139', '410', '1374', '5575', '2186', '170', '2632', '2473', '54971', '12409', '2810', '972', '1584', '48493', '377', '19772', '2435', '2567', '19829', '2862', '2851', '2589', '2892', '1735', '1759', '23786', '24587', '1198', '1521', '2826', '27846', '61992', '299', '212', '2795', '50057', '5144', '25601', '37382', '41338', '2701', '413', '1110', '2602', '24480', '23722', '440', '796', '23930', '24505', '24458', '24293', '745', '615', '1240', '12350', '57364', '35767', '2523', '2415', '25748', '24060', '52189', '1510', '46455', '22919', '2733', '23418', '1329', '1390', '1274', '62707', '25368', '13000', '128', '1661', '2184', '51101', '16782', '31466', '39192', '2060', '2705', '2513', '52188', '526', '495', '101', '109', '81', '2337', '2195', '39096', '25727', '2597', '2678', '2666', '209', '1010', '573', '1175', '12971', '1641', '20269', '49067', '350', '455', '1606', '50641', '1859', '58515', '24485', '38222', '19322', '2440', '2481', '2611', '877', '1796', '2485', '224', '2069', '44266', '3891', '917', '31691', '23723', '23772', '59149', '57059', '61119', '1551', '599', '534', '23895', '840', '1418', '59155', '2581', '10266', '23916', '1979', '2490', '24724', '1321', '2627', '1326', '1598', '45971', '29779', '23', '608', '1998', '1930', '1453', '6017', '2793', '46384', '59148', '988', '32422', '3618', '2650', '1857', '344', '930', '751', '51105', '48268', '41404', '24131', '61579', '24491', '464', '934', '1629', '935', '62997', '204', '1896', '24361', '63345', '2850', '1276', '68', '30307', '24106', '20324', '24255', '35497', '845', '40713', '2760', '11486', '925', '541', '40712', '24436', '63674', '1081', '34', '365', '2734', '23917', '23921', '23919', '21753', '196', '708', '23818', '1438', '10565', '8866', '527', '60', '1989', '45172', '24321', '21894', '61548', '35353', '2006', '854', '1104', '24183', '982', '34369', '50855', '44698', '37122', '24472', '2042', '2442', '1155', '1691', '2596', '2397', '746', '98', '2735', '58704', '24363', '1116', '1048', '347', '1715', '1062', '2845', '53270', '457', '2527', '3620', '2600', '12353', '2664', '2464', '7', '2048', '2502', '1491', '11087', '483', '1170', '26922', '58361', '2204', '19927', '24185', '726', '282', '201', '838', '1603', '349', '17846', '46601', '33', '811', '1265', '1890', '1542', '294', '36217', '23248', '921', '184', '59048', '2162', '235', '400', '649', '2700', '941', '45409', '31006', '23773', '1568', '2035', '1507', '2863', '2818', '2727', '900', '13022', '1375', '8589', '3595', '24468', '30204', '290', '2777', '3596', '1318', '1962', '243', '296', '6602', '669', '605', '9126', '1646', '2563', '64', '52017', '62214', '63120', '32250', '1243', '2119', '1653', '37861', '85', '313', '217', '43362', '45537', '31135', '24295', '18812', '1658', '37', '1038', '1993', '1833', '21803', '1425', '49163', '39095', '1548', '1293', '42464', '50009', '1621', '1566', '24105', '1513', '2628', '2621', '2197', '8420', '1573', '24067', '1800', '1494', '1404', '1743', '1692', '1609', '610', '268', '220', '770', '1648', '44386', '46519', '199', '2633', '23807', '50987', '24158', '24147', '1420', '45466', '747', '1071', '30301', '24396', '21932', '32054', '2537', '11976', '1875', '49281', '43414', '210', '59980', '442', '385', '586', '1241', '1077', '62914', '63295', '2300', '48104', '1169', '1747', '1783', '105', '273', '2141', '876', '1904', '1591', '48856', '381', '267', '488', '2805', '643', '1951', '15862', '58884', '686', '3625', '21922', '653', '2658', '728', '50791', '2814', '2064', '59152', '49046', '1673', '970', '4856', '2142', '54838', '26265', '1516', '1902', '766', '1582', '1560', '1004', '1055', '1665', '2585', '2644', '61357', '607', '50792', '1939', '60926', '1607', '1344', '191', '2066', '41911', '24865', '2394', '868', '1065', '288', '45538', '24092', '1405', '1602', '2206', '56368', '327', '33923', '23955', '49223', '20082', '533', '1632', '25103', '2840', '2873', '1863', '24298', '1933', '1381', '1279', '1864', '24323', '2159', '38286', '2565', '1872', '2367', '2663', '2172', '937', '2094', '8529', '2639', '463', '363', '1301', '1874', '1417', '1786', '375', '1045', '1772', '234', '2011', '94', '762', '37852', '1919', '1982', '272', '2207', '24368', '24130', '735', '4233', '21906', '44879', '24220', '28104', '24069', '23762', '60405', '2779', '2097', '1209', '1049', '1659', '24316', '24490', '1261', '1013', '292', '1208', '767', '2194', '13923', '12352', '394', '743', '738', '9048', '2056', '2409', '2117', '1283', '316', '563', '61', '2150', '23973', '24063', '950', '1084', '1189', '1137', '38972', '24166', '1254', '2004', '62627', '1467', '515', '90', '48', '2671', '2027', '1622', '42931', '24393', '24445', '18094', '591', '39912', '41454', '24062', '45539', '2343', '1412', '25595', '17922', '23959', '1888', '927', '1102', '24443', '31377', '48848', '2385', '2741', '26', '2000', '12818', '691', '12650', '2256', '46598', '2896', '1694', '1771', '2074', '1220', '2277', '19175', '2174', '2524', '2578', '1151', '575', '473', '12385', '50989', '11337', '42946', '1087', '167', '2258', '1753', '46597', '2622', '2262', '1533', '847', '1076', '2138', '19830', '1814', '777', '1484', '1519', '1215', '1707', '26926', '46459', '2416', '48545', '1885', '8417', '3694', '2390', '2395', '26266', '2153', '53155', '1428', '1188', '641', '3632', '2459', '2139', '1270', '480', '23878', '2877', '2867', '36809', '1234', '10365', '21924', '2254', '2019', '24481', '1176', '23845', '41330', '2377', '2287', '13055', '14608', '2318', '6493', '831', '6668', '1059', '992', '1222', '63459', '2043', '2015', '7394', '10750', '48638', '41913', '2369', '52194', '1235', '1073', '688', '2274', '1180', '60081', '2852', '2858', '23981', '1477', '17240', '1406', '779', '889', '24492', '15289', '2263', '2098', '5143', '351', '269', '32265', '23727', '38971', '24462', '1080', '1190', '1616', '38337', '24424', '12966', '15696', '1266', '14439', '2155', '26333', '451', '24199', '32071', '44345', '1561', '9508', '312', '5130', '2812', '15112', '12459', '1779', '2296', '1351', '39584', '21911', '1889', '2359', '32249', '310', '1821', '8427', '24463', '2034', '4854', '861', '15471', '954', '279', '2407', '2167', '2284', '1031', '1482', '1211', '1807', '1515', '8425', '22817', '585', '41910', '2047', '13029', '42698', '1852', '19126', '45970', '427', '1695', '984', '44388', '9781', '17909', '507', '722', '9219', '116', '1012', '2802', '6069', '16913', '2438', '1858', '23734', '20470', '1545', '13591', '24447', '21147', '1145', '62794', '1166', '23980', '645', '38075', '553', '2229', '1120', '271', '17845', '208', '391', '2725', '24301', '278', '1708', '1790', '55793', '41457', '2010', '2248', '893', '776', '772', '5498', '24603', '1138', '60079', '24072', '23318', '24556', '358', '49359', '28521', '1792', '26779', '1454', '2403', '1567', '760', '1057', '46583', '1452', '1292', '48499', '23515', '37787', '2738', '31244', '1546', '1162', '31813', '1941', '1729', '2536', '46250', '48857', '1345', '1334', '928', '383', '1860', '1987', '8590', '9033', '1587', '1262', '953', '434', '588', '1159', '654', '2451', '25133', '966', '1664', '717', '9502', '2478', '1697', '49221', '26707', '58015', '3365', '23841', '15814', '24370', '485', '19061', '2544', '59159', '1802', '1203', '1217', '1422', '308', '37870', '23863', '1693', '1719', '1574', '24351', '45300', '2224', '848', '41037', '30298', '24482', '2264', '11974', '2334', '844', '21743', '20467', '24466', '2722', '2571', '1887', '37856', '27952', '432', '24281', '23843', '1479', '1991', '24033', '2763', '23174', '395', '2253', '1737', '1625', '26257', '1900', '46517', '20633', '630', '1161', '31849', '1932', '21307', '9985', '519', '24078', '24330', '10361', '24340', '2257', '254', '21381', '31745', '50637', '2673', '2222', '24435', '1328', '2209', '7395', '2461', '878', '943', '1797', '24053', '64598', '13476', '50061', '42629', '1638', '15452', '11089', '9989', '3573', '21354', '1435', '462', '1043', '23998', '45837', '2488', '2687', '2553', '3114', '2569', '2211', '2566', '239', '500', '23918', '1086', '228', '2108', '1431', '36110', '1392', '453', '2169', '25671', '2804', '705', '30295', '1514', '2643', '851', '642', '5138', '1362', '1469', '1462', '2387', '565', '1714', '1717', '1228', '2182', '60774', '1774', '59050', '5140', '1572', '2772', '15149', '29064', '2901', '9125', '9470', '2510', '2144', '806', '9469', '20465', '1713', '2173', '50930', '23791', '2829', '1068', '1611', '23751', '1557', '8107', '2371', '13019', '1258', '119', '1654', '1332', '3579', '19756', '46383', '15694', '15284', '1041', '1164', '24483', '287', '2218', '31814', '1336', '26767', '1712', '2304', '709', '2376', '24219', '2398', '50856', '2508', '29775', '301', '71', '1586', '36408', '7592', '2215', '977', '1272', '2623', '5141', '1541', '10043', '1924', '10263', '13518', '2853', '1294', '2154', '32015', '2219', '54754', '2445', '58706', '5156', '2400', '46600', '1192', '1135', '511', '2828', '24428', '24416', '28318', '3583', '261', '12946', '1517', '248', '2861', '1880', '1769', '41395', '2392', '1804', '49433', '41225', '20447', '19827', '33885', '2559', '1323', '823', '2326', '3591', '1382', '25572', '37746', '31243', '1556', '27022', '2562', '153', '26264', '26913', '24230', '20083', '60581', '46529', '1953', '2880', '58891', '2809', '8787', '2240', '1069', '73', '2032', '52396', '1441', '2295', '1300', '366', '2363', '51071', '4062', '12066', '62062', '1255', '19892', '15275', '1245', '10578', '2181', '43293', '57311', '2149', '1745', '1897', '788', '10358', '255', '1558', '1599', '2668', '37123', '13316', '2619', '2234', '2059', '1442', '1230', '78', '59153', '11685', '2836', '918', '1958', '31238', '49324', '2605', '10375', '10367', '1992', '1834', '23915', '57917', '9475', '566', '1388', '759', '46595', '60193', '1400', '63106', '10550', '2140', '25029', '2335', '2148', '426', '2457', '43226', '1115', '2681', '2306', '2038', '49130', '46530', '21928', '1594', '1380', '1009', '1005', '24402', '1663', '2327', '1915', '18813', '2018', '24168', '48610', '12824', '221', '1613', '23903', '3680', '1955', '1202', '5137', '1983', '2111', '9463', '9505', '2525', '112', '784', '680', '62679', '2857', '63318', '2104', '41905', '2822', '24190', '2746', '27691', '5133', '1931', '1578', '635', '944', '1312', '42088', '1768', '24203', '2431', '2161', '1754', '828', '1823', '2383', '1818', '23923', '411', '771', '63666', '63589', '1448', '27622', '2112', '2365', '562', '30', '2838', '1903', '2364', '2815', '11684', '1773', '1092', '1841', '24126', '20468', '20365', '2719', '548', '525', '1119', '1537', '2556', '203', '61991', '37757', '2737', '53588', '2729', '51990', '16294', '237', '424', '2521', '63817', '19822', '1763', '2846', '2336', '694', '2782', '1720', '21', '2328', '23658', '2652', '57706', '1238', '48498', '9509', '1725', '1315', '692', '618', '38268', '3574', '2126', '10727', '8947', '24260', '1219', '1836', '1249', '2895', '25571', '915', '2535', '2894', '2179', '1801', '2884', '24020', '2800', '1934', '20462', '54214', '15555', '736', '2864', '2090', '2036', '2002', '24016', '60504', '1416', '2353', '2718', '2674', '1008', '354', '721', '1401', '1290', '1640', '13016', '7060', '43183', '430', '211', '2706', '19784', '19133', '8426', '19138', '6021', '787', '1917', '2341', '33880', '6061', '19140', '10373', '1682', '24036', '23789', '1856', '44', '2552', '24423', '1742', '958', '2030', '9614', '13017', '393', '41906', '42783', '13010', '13009', '13011', '13012', '13013', '24322', '61902', '2693', '52813', '49446', '1961', '10644', '2868', '2068', '2475', '1789', '1067', '1327', '1366', '46594', '1553', '2212', '38913', '20268', '55058', '1569', '980', '2164', '619', '477', '1876', '2176', '604', '1348', '149', '498', '801', '2089', '8298', '3363', '24208', '487', '113', '62782', '666', '2193', '12812', '1383', '1132', '44696', '15214', '3696', '1793', '21148', '22', '2293', '6379', '2712', '2754', '24171', '1460', '60416', '42819', '7825', '30108', '52812', '24542', '13027', '59158', '2463', '1307', '1257', '2751', '15699', '20554', '19816', '17239', '1143', '2872', '2789', '13523', '2202', '3614', '2333', '1314']`

"""