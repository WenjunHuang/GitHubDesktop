from send2trash import send2trash

class AppShell:
    def move_item_to_trash(self,path:str)->bool:
        send2trash(path)

    def beep(self):
        pass

    async def open_external(self,path:str)->bool:
        pass

    def open_item(self,path:str)->bool:
        pass

    def show_item_in_folder(self,path:str):
        pass