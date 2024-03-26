class Helper:
    def check_input_string(self, input_string: str) -> bool:
        if len(input_string) != 9:
            return False
        
        seen = set()
        for char in input_string:
            if char.isdigit() and char != '9' and char not in seen:
                seen.add(char)
            else:
                return False

        return len(seen) == 9
