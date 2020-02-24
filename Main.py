from Module import WUI
from Control import ptt_ctrl

class Main:
    def __init__(self):
        self.wui = WUI.WUI("", "", exit_time=999999, port=6688)
        self.ctrl = ptt_ctrl.CTRL(wui=self.wui)
        self.WS_Hook()
        self.wui.Start_WS(start_browser=0)


    def WS_Hook(self):
        self.wui.Add_Recv_Msg_Hook("Ptt_List", self.ctrl.Ptt_List_fn)


if __name__ == "__main__":
    obj = Main()