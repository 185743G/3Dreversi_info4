from Constants import ThreeD, X, Y, Z


class In_Out_put:

    def __init__(self,val):
        self.QUIT = -1
        self.PASS = -2
        self.COMMAND = 2
        self.ONEMORE = 3
        self.PCQUIT = False
        if val == 0:
            self.LENGTH = self.select_size()
        else:
            self.LENGTH = (val+2)*2

    def is_position(self, char):
        result = False
        try:
            chk_char = int(char)
        except ValueError as e:
            return result
        for i in range(self.LENGTH - 2):
            if chk_char is i + 1:
                result = True
        return result

    def read_command(self, val):
        quit_or_pass_or_command = -1  # error flag
        if val == "quit":
            quit_or_pass_or_command = self.QUIT
        elif val == "pass":
            quit_or_pass_or_command = self.PASS
        elif self.is_position(val):
            quit_or_pass_or_command = self.COMMAND
        else:
            quit_or_pass_or_command = self.ONEMORE
        return quit_or_pass_or_command

    def read(self):
        i = 0
        coordinate_input = [0] * ThreeD
        read_command_up = True
        while read_command_up:
            if i == X:
                print("x座標を入力してください")
            elif i == Y:
                print("y座標を入力してください")
            elif i == Z:
                print("z座標を入力してください")
            val = input()

            if self.read_command(val) == self.QUIT:
                self.PCQUIT = True
                break
            if self.read_command(val) == self.PASS:
                coordinate_input = [self.PASS] * ThreeD
                break
            if self.read_command(val) == self.COMMAND:
                coordinate_input[i] = int(val)
                i = i + 1
            if self.read_command(val) == self.ONEMORE:
                print("指定した数または文字は不正です。")
            if i == 3:
                read_command_up = False
        return coordinate_input

    def select_size(self):
        size = 0

        print("ゲーム盤のサイズを左記の数字より指定してください　小{1,2,3}大")
        val = input()
        while True:
            value_is_int = True
            try:
                chk_char = int(val)
            except ValueError as e:
                value_is_int = False
            if value_is_int:
                if int(val) == 3 or int(val) == 2 or int(val) == 1:
                    break
            print("不正な値です")
            val = input()

        size = (int(val) + 2) * 2
        return size
