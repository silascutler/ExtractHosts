from string import printable, ascii_lowercase, ascii_uppercase, digits
from re import compile, IGNORECASE, S
from os import listdir
from os.path import isfile, isdir, join, abspath
from socket import inet_pton, AF_INET6, error as socket_error

domain_characters = ascii_lowercase + ascii_uppercase + digits + "-.:"
is_domain_regex_strict = compile("([a-z0-9][a-z0-9\-]{0,61}[a-z0-9]\.)+[a-z0-9][a-z0-9\-]*[a-z0-9]")
is_domain_regex = compile("([a-z0-9][a-z0-9\-]{0,61}[a-z0-9]\.)+[a-z0-9][a-z0-9\-]*[a-z0-9]", IGNORECASE)
is_ipv4_regex = compile("[1-2]?[0-9]?[0-9]\.[1-2]?[0-9]?[0-9]\.[1-2]?[0-9]?[0-9]\.[1-2]?[0-9]?[0-9]")
is_ipv6_regex = compile("((([0-9A-Fa-f]{1,4}:){7}([0-9A-Fa-f]{1,4}|:))|(([0-9A-Fa-f]{1,4}:){6}(:[0-9A-Fa-f]{1,4}|((25[0"
                        "-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:)"
                        "{5}(((:[0-9A-Fa-f]{1,4}){1,2})|:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|["
                        "1-9]?\d)){3})|:))|(([0-9A-Fa-f]{1,4}:){4}(((:[0-9A-Fa-f]{1,4}){1,3})|((:[0-9A-Fa-f]{1,4})?:((2"
                        "5[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,"
                        "4}:){3}(((:[0-9A-Fa-f]{1,4}){1,4})|((:[0-9A-Fa-f]{1,4}){0,2}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d"
                        ")(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){2}(((:[0-9A-Fa-f]{1,4}){1"
                        ",5})|((:[0-9A-Fa-f]{1,4}){0,3}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1"
                        "-9]?\d)){3}))|:))|(([0-9A-Fa-f]{1,4}:){1}(((:[0-9A-Fa-f]{1,4}){1,6})|((:[0-9A-Fa-f]{1,4}){0,4}"
                        ":((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)){3}))|:))|(:(((:[0-9A-"
                        "Fa-f]{1,4}){1,7})|((:[0-9A-Fa-f]{1,4}){0,5}:((25[0-5]|2[0-4]\d|1\d\d|[1-9]?\d)(\.(25[0-5]|2[0-"
                        "4]\d|1\d\d|[1-9]?\d)){3}))|:)))(%.+)?", IGNORECASE | S)
tlds = ["AC", "ACADEMY", "ACTOR", "AD", "AE", "AERO", "AF", "AG", "AGENCY", "AI", "AL", "AM", "AN", "AO", "AQ", "AR",
        "ARPA", "AS", "ASIA", "AT", "AU", "AW", "AX", "AZ", "BA", "BAR", "BARGAINS", "BB", "BD", "BE", "BERLIN", "BEST",
        "BF", "BG", "BH", "BI", "BID", "BIKE", "BIZ", "BJ", "BLUE", "BM", "BN", "BO", "BOUTIQUE", "BR", "BS", "BT",
        "BUILD", "BUILDERS", "BUZZ", "BV", "BW", "BY", "BZ", "CA", "CAB", "CAMERA", "CAMP", "CARDS", "CAREERS", "CAT",
        "CATERING", "CC", "CD", "CENTER", "CEO", "CF", "CG", "CH", "CHEAP", "CHRISTMAS", "CI", "CK", "CL", "CLEANING",
        "CLOTHING", "CLUB", "CM", "CN", "CO", "CODES", "COFFEE", "COM", "COMMUNITY", "COMPANY", "COMPUTER", "CONDOS",
        "CONSTRUCTION", "CONTRACTORS", "COOL", "COOP", "CR", "CRUISES", "CU", "CV", "CW", "CX", "CY", "CZ", "DANCE",
        "DATING", "DE", "DEMOCRAT", "DIAMONDS", "DIRECTORY", "DJ", "DK", "DM", "DNP", "DO", "DOMAINS", "DZ", "EC",
        "EDU", "EDUCATION", "EE", "EG", "EMAIL", "ENTERPRISES", "EQUIPMENT", "ER", "ES", "ESTATE", "ET", "EU", "EVENTS",
        "EXPERT", "EXPOSED", "FARM", "FI", "FISH", "FJ", "FK", "FLIGHTS", "FLORIST", "FM", "FO", "FOUNDATION", "FR",
        "FUTBOL", "GA", "GALLERY", "GB", "GD", "GE", "GF", "GG", "GH", "GI", "GIFT", "GL", "GLASS", "GM", "GN", "GOV",
        "GP", "GQ", "GR", "GRAPHICS", "GS", "GT", "GU", "GUITARS", "GURU", "GW", "GY", "HK", "HM", "HN", "HOLDINGS",
        "HOLIDAY", "HOUSE", "HR", "HT", "HU", "ID", "IE", "IL", "IM", "IMMOBILIEN", "IN", "INDUSTRIES", "INFO", "INK",
        "INSTITUTE", "INT", "INTERNATIONAL", "IO", "IQ", "IR", "IS", "IT", "JE", "JM", "JO", "JOBS", "JP", "KAUFEN",
        "KE", "KG", "KH", "KI", "KIM", "KITCHEN", "KIWI", "KM", "KN", "KOELN", "KP", "KR", "KRED", "KW", "KY", "KZ",
        "LA", "LAND", "LB", "LC", "LI", "LIGHTING", "LIMO", "LINK", "LK", "LR", "LS", "LT", "LU", "LUXURY", "LV", "LY",
        "MA", "MAISON", "MANAGEMENT", "MANGO", "MARKETING", "MC", "MD", "ME", "MENU", "MG", "MH", "MIL", "MK", "ML",
        "MM", "MN", "MO", "MOBI", "MODA", "MONASH", "MP", "MQ", "MR", "MS", "MT", "MU", "MUSEUM", "MV", "MW", "MX",
        "MY", "MZ", "NA", "NAGOYA", "NAME", "NC", "NE", "NET", "NEUSTAR", "NF", "NG", "NI", "NINJA", "NL", "NO", "NP",
        "NR", "NU", "NZ", "OKINAWA", "OM", "ONION", "ONL", "ORG", "PA", "PARTNERS", "PARTS", "PE", "PF", "PG", "PH",
        "PHOTO", "PHOTOGRAPHY", "PHOTOS", "PICS", "PINK", "PK", "PL", "PLUMBING", "PM", "PN", "POST", "PR", "PRO",
        "PRODUCTIONS", "PROPERTIES", "PS", "PT", "PUB", "PW", "PY", "QA", "QPON", "RE", "RECIPES", "RED", "RENTALS",
        "REPAIR", "REPORT", "REVIEWS", "RICH", "RO", "RS", "RU", "RUHR", "RW", "SA", "SB", "SC", "SD", "SE", "SEXY",
        "SG", "SH", "SHIKSHA", "SHOES", "SI", "SINGLES", "SJ", "SK", "SL", "SM", "SN", "SO", "SOCIAL", "SOLAR",
        "SOLUTIONS", "SR", "ST", "SU", "SUPPLIES", "SUPPLY", "SUPPORT", "SV", "SX", "SY", "SYSTEMS", "SZ", "TATTOO",
        "TC", "TD", "TECHNOLOGY", "TEL", "TF", "TG", "TH", "TIENDA", "TIPS", "TJ", "TK", "TL", "TM", "TN", "TO",
        "TODAY", "TOKYO", "TOOLS", "TP", "TR", "TRAINING", "TRAVEL", "TT", "TV", "TW", "TZ", "UA", "UG", "UK", "UNO",
        "US", "UY", "UZ", "VA", "VACATIONS", "VC", "VE", "VENTURES", "VG", "VI", "VIAJES", "VILLAS", "VISION", "VN",
        "VOTE", "VOTING", "VOTO", "VOYAGE", "VU", "WANG", "WATCH", "WED", "WF", "WIEN", "WIKI", "WORKS", "WS",
        "XN--3BST00M", "XN--3DS443G", "XN--3E0B707E", "XN--45BRJ9C", "XN--55QW42G", "XN--55QX5D", "XN--6FRZ82G",
        "XN--6QQ986B3XL", "XN--80AO21A", "XN--80ASEHDB", "XN--80ASWG", "XN--90A3AC", "XN--C1AVG", "XN--CG4BKI",
        "XN--CLCHC0EA0B2G2A9GCD", "XN--D1ACJ3B", "XN--FIQ228C5HS", "XN--FIQ64B", "XN--FIQS8S", "XN--FIQZ9S",
        "XN--FPCRJ9C3D", "XN--FZC2C9E2C", "XN--GECRJ9C", "XN--H2BRJ9C", "XN--I1B6B1A6A2E", "XN--IO0A7I", "XN--J1AMH",
        "XN--J6W193G", "XN--KPRW13D", "XN--KPRY57D", "XN--L1ACC", "XN--LGBBAT1AD8J", "XN--MGB9AWBF", "XN--MGBA3A4F16A",
        "XN--MGBAAM7A8H", "XN--MGBAB2BD", "XN--MGBAYH7GPA", "XN--MGBBH1A71E", "XN--MGBC0A9AZCG", "XN--MGBERP4A5D4AR",
        "XN--MGBX4CD0AB", "XN--NGBC5AZD", "XN--NQV7F", "XN--NQV7FS00EMA", "XN--O3CW4H", "XN--OGBPF8FL", "XN--P1AI",
        "XN--PGBS0DH", "XN--Q9JYB4C", "XN--RHQV96G", "XN--S9BRJ9C", "XN--UNUP4Y", "XN--WGBH1C", "XN--WGBL6A",
        "XN--XKC2AL3HYE2A", "XN--XKC2DL3A5EE0H", "XN--YFRO4I67O", "XN--YGBI2AMMX", "XN--ZFR164B", "XXX", "XYZ", "YE",
        "YT", "ZA", "ZM", "ZONE", "ZW"]


def get_version():
    """
    Function to manually update for each version
    """
    return "1.3.0"


def extract_ipv4(to_check, strict=False):
    """
    Extracts any ipv4 address from the supplied string
    """
    r = is_ipv4_regex.search(to_check)
    if r:
        return r.group(0)
    return None


def is_valid_ipv6(to_check):
    """
    Since the ipv6 detection is kinda iffy at the moment, we should be able to do kernel level checks
    """
    try:
        inet_pton(AF_INET6, to_check)
        return True
    except socket_error:
        return False


def extract_ipv6(to_check, strict=False):
    """
    Extracts any ipv6 address from the supplied string
    """
    r = is_ipv6_regex.search(to_check)
    if r and is_valid_ipv6(r.group(0)):
        return r.group(0)
    return None


def extract_domain(to_check, strict=False):
    """
    Extracts any domain from the supplied string
    """
    if strict:
        r = is_domain_regex_strict.search(to_check)
    else:
        r = is_domain_regex.search(to_check)
    if r and has_valid_tld(r.group(0)):
        return r.group(0)
    return None


def has_valid_tld(to_check):
    """
    Checks if supposed domain has a valid TLD
    """
    if to_check.find(".") == -1:
        return False
    if to_check[to_check.rfind(".") + 1:].upper() in tlds:
        return True
    return False


def extract_strings(data, minimum=4, charset=printable):
    """
    Gets all strings based on the supplied character set
    Can work on binary data (PE files, etc)
    """
    # states
    #   0 - None
    #   1 - ASCII or UTF-16LE
    #   2 - ASCII
    #   3 - UTF-16LE - expecting character
    #   4 - UTF-16LE - expecting null
    state = 0
    result = ""
    for c in data:
        if state == 0:
            if c in charset:
                result += c
                state = 1
                continue
            continue
        elif state == 1:
            if c == 0x00:
                state = 3
                continue
            elif c in charset:
                result += c
                continue
        elif state == 2:
            if c in charset:
                result += c
                continue
        elif state == 3:
            if c in charset:
                result += c
                state = 4
                continue
        elif state == 4:
            if c == 0x00:
                state = 3
                continue
        if len(result) >= minimum:
            yield result
        result = ""
        state = 0
    if len(result) >= minimum:
        yield result


def extract_strings_from_file_handle(fh, minimum=4, charset=printable):
    """
    Gets all strings based on the supplied character set
    Can work on binary data (PE files, etc)
    """
    # states
    #   0 - None
    #   1 - ASCII or UTF-16LE
    #   2 - ASCII
    #   3 - UTF-16LE - expecting character
    #   4 - UTF-16LE - expecting null
    state = 0
    result = ""
    c = fh.read(1)
    while c != "":
        if state == 0:
            if c in charset:
                result += c
                state = 1
                c = fh.read(1)
                continue
            c = fh.read(1)
            continue
        elif state == 1:
            if ord(c) == 0x00:
                state = 3
                c = fh.read(1)
                continue
            elif c in charset:
                result += c
                state = 2
                c = fh.read(1)
                continue
        elif state == 2:
            if c in charset:
                result += c
                c = fh.read(1)
                continue
        elif state == 3:
            if c in charset:
                result += c
                state = 4
                c = fh.read(1)
                continue
        elif state == 4:
            if ord(c) == 0x00:
                state = 3
                c = fh.read(1)
                continue
        if len(result) >= minimum:
            yield result
        result = ""
        state = 0
        c = fh.read(1)
    if len(result) >= minimum:
        yield result


def extract_hosts_from_string(to_check, strict_domains):
    """
    Extracts any hosts from strings
    """
    for s in extract_strings(to_check, 3, domain_characters):
        data = extract_domain(s, strict_domains)
        if data:
            yield data
        data = extract_ipv4(s, strict_domains)
        if data:
            yield data
        data = extract_ipv6(s, strict_domains)
        if data:
            yield data


def extract_hosts_from_file_handle(fh, strict_domains, check_ipv4, check_ipv6, check_domain):
    """
    Extracts any hosts from file handle
    """
    for s in extract_strings_from_file_handle(fh, 3, domain_characters):
        if check_domain:
            data = extract_domain(s, strict_domains)
            if data:
                yield data
        if check_ipv4:
            data = extract_ipv4(s, strict_domains)
            if data:
                yield data
        if check_ipv6:
            data = extract_ipv6(s, strict_domains)
            if data:
                yield data


def _test_extract_hosts_from_string():
    expected_back = [
        "FE80::0202:B3FF:FE1E:8329",
        "FE80:0000:0000:0000:0202:B3FF:FE1E:8329",
        "2001:db8::ff00:42:8329",
        "::1",
        "0.0.0.0",
        "127.0.0.1",
        "255.255.255.255",
        "khi46.sxtbqk.uh6coh.h0khpow.info",
        "recipesforourdailybread.com",
    ]

    for host in extract_hosts_from_string("\r\n".join(expected_back), True):
        if host not in expected_back:
            raise Exception("Not value in supplied set")
        expected_back.remove(host)
    if len(expected_back) != 0:
        raise Exception("Not all values returned")
    print "Passed"


def scan_file_handle(file_handle, strict_domains, check_ipv4, check_ipv6, check_domain):
    for host in extract_hosts_from_file_handle(file_handle, strict_domains, check_ipv4, check_ipv6, check_domain):
        yield host


def scan_paths(paths, recursive, strict_domains, check_ipv4, check_ipv6, check_domain):
    while len(paths) != 0:
        try:
            file_path = abspath(paths[0])
            del paths[0]
            if isfile(file_path):
                try:
                    with open(file_path, mode='rb') as file_handle:
                        for host in scan_file_handle(file_handle, strict_domains, check_ipv4, check_ipv6, check_domain):
                            yield (file_path, host)
                except IOError:
                    pass
            elif isdir(file_path):
                for p in listdir(file_path):
                    try:
                        p = join(file_path, p)
                        if isfile(p) or (isdir(p) and recursive):
                            paths.append(p)
                    except IOError:
                        pass
        except IOError:
            pass