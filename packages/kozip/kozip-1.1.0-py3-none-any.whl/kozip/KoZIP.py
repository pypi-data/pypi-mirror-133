import json
import os
import re

class KoZIP:
    def __init__(self):
        self.old_zip_file = os.path.join(os.path.dirname(__file__), "old_zip.json")
        self.new_zip_file = os.path.join(os.path.dirname(__file__), "new_zip.json")

        self.old_zip = None
        self.new_zip = None

        self.new_zipcode_masked = {}

    def _readlines(self, file):
        for enc in ["utf8", "utf-8-sig", "ansi", "cp949", "euc-kr"]:
            try:
                with open(file, "r", encoding=enc) as f:
                    lines = f.readlines()

                return lines
            except:
                continue
    
        raise Exception("Encoding not found:", file)
    
    def _build(self, dir):
        data = {}
        for file in [f"{dir}/{file}" for file in os.listdir(dir) if file.endswith(".txt")]:
            for line in self._readlines(file)[1:]:
                splits = line.split("|")
                zipcode = splits[0]

                loc1 = splits[1] # 시도
                loc2 = splits[3] # 시군구
                loc3 = splits[8] # 도로명

                loc4 = splits[11] + ('' if (len(splits[12]) == 0 or splits[12] == "0") else ('-' + splits[12])) # 건물번호본번-건물번호부번
                if len(loc4) != 0:
                    loc3 += ' ' + loc4

                loc5 = splits[5] + splits[17] + ('' if len(splits[18]) == 0 else (' ' + splits[18])) # 읍면동, 리
                if len(loc5) != 0:
                    loc3 += '|' + loc5

                if zipcode not in data.keys():
                    data[zipcode] = dict()

                if loc1 not in data[zipcode].keys():
                    data[zipcode][loc1] = dict()

                if loc2 not in data[zipcode][loc1].keys():
                    data[zipcode][loc1][loc2] = []

                data[zipcode][loc1][loc2].append(loc3)

        for zipcode in data.keys():
            for loc1 in data[zipcode].keys():
                for loc2 in data[zipcode][loc1].keys():
                    data[zipcode][loc1][loc2].sort()

        self.new_zip = data
        
        with open("new_zip.json", "w") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    
    def _getData(self, type="new"):
        assert type in ["old", "new"], "Invalid param: type"

        if type == "old":
            if self.old_zip == None:
                self.old_zip = json.loads(''.join(self._readlines(self.old_zip_file)))
            return self.old_zip
        else:
            if self.new_zip == None:
                self.new_zip = json.loads(''.join(self._readlines(self.new_zip_file)))
            return self.new_zip

    def _getAddr(self, data, zipcode, depth, format):
        if depth in [1, "1", "시도"]:
            result = []
            for loc1 in data[zipcode].keys():
                if format == "string":
                    result.append(loc1)
                    
                else: # format == "list"
                    result.append([loc1])
                    
        elif depth in [2, "2", "시군구"]:
            result = []
            for loc1 in data[zipcode].keys():
                for loc2 in data[zipcode][loc1]:
                    if format == "string":
                        string = loc1
                        if len(loc2) != 0:
                            string += ' ' + loc2
                            
                        result.append(string)
                        
                    else: # format == "list"
                        result.append([loc1, loc2])
                        
        elif depth in [3, "3", "도로명"]:
            result = []
            for loc1 in data[zipcode].keys():
                for loc2 in data[zipcode][loc1]:
                    for loc3 in data[zipcode][loc1][loc2]:
                        loc3 = loc3.split("|")[0]
                        if format == "string":
                            string = loc1
                            if len(loc2) != 0:
                                string += ' ' + loc2
                            if len(loc3) != 0:
                                string += ' ' + loc3
                                
                            result.append(string)
                            
                        else: # format == "list"
                            result.append([loc1, loc2, loc3])
                            
        elif depth in [4, "4", "full"]:
            result = []
            for loc1 in data[zipcode].keys():
                for loc2 in data[zipcode][loc1]:
                    for loc3 in data[zipcode][loc1][loc2]:
                        loc3, loc4 = loc3.split("|")
                        if len(loc4) != 0:
                            loc3 += ' ' + f"({loc4})"
                            
                        if format == "string":
                            string = loc1
                            if len(loc2) != 0:
                                string += ' ' + loc2
                            if len(loc3) != 0:
                                string += ' ' + loc3
                            
                            result.append(string)
                            
                        else: # format == "list"
                            result.append([loc1, loc2, loc3])
        
        return result

    def _mergeDict(self, dest_dict, src_dict):
        if type(dest_dict) is list and type(src_dict) is list:
            dest_dict = list(set(dest_dict + src_dict))
            return
        else:
            for key in src_dict.keys():
                if key not in dest_dict.keys():
                    dest_dict[key] = src_dict[key]
                else:
                    self._mergeDict(dest_dict[key], src_dict[key])
            return

    def ZIPtoAddr(self, zipcode, depth=2, format="string"):
        assert depth in [1, "1", "시도", 2, "2", "시군구", 3, "3", "도로명", 4, "4", "full"], "Invalid param: depth"
        assert format in ["list", "string"], "Invalid param: format"

        zipcode = str(zipcode)
        if re.fullmatch("\d{5}", zipcode):
            data = self._getData("new")
        elif re.fullmatch("\d{3}-\d{3}", zipcode):
            data = self._getData("old")
        elif re.fullmatch("\d{6}", zipcode):
            zipcode = zipcode[0:3] + '-' + zipcode[3:6]
            data = self._getData("old")
        else:
            raise Exception("Invalid param: zipcode")
        
        return self._getAddr(data, zipcode, depth, format)

    def maskedZIPtoAddr(self, masked_zipcode, masking_letter="*", depth=1, format="string"):
        assert type(masking_letter) is str and len(masking_letter) == 1, "Invalid param: masking_letter"
        assert type(masked_zipcode) is str and len(masked_zipcode) == 5, "Invalid param: masked_zipcode"
        assert len([x for x in masked_zipcode if not (x.isdigit() or x == masking_letter)]) == 0, "Invalid param: masked_zipcode"
        assert depth in [1, "1", "시도", 2, "2", "시군구", 3, "3", "도로명", 4, "4", "full"], "Invalid param: depth"
        assert format in ["list", "string"], "Invalid param: format"

        full_data = self._getData("new")
        masked_zipcode = masked_zipcode.replace(masking_letter, "*")

        masked_type = "".join([("0" if c.isdigit() else "*") for c in masked_zipcode])
        if masked_type not in self.new_zipcode_masked.keys():
            self.new_zipcode_masked[masked_type] = dict()
            target = self.new_zipcode_masked[masked_type]

            for key, value in full_data.items():
                masked_key = "".join([("*" if c == "*" else key[i]) for i, c in enumerate(masked_type)])
                if masked_key not in target.keys():
                    target[masked_key] = {}
                
                self._mergeDict(target[masked_key], value)

        return self._getAddr(self.new_zipcode_masked[masked_type], masked_zipcode, depth, format)
