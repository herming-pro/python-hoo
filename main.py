import oo

main = oo.callback_object_main()
main.set_debuglevel(0)
main.showName = False
#新版讀取 callback 結束直接去read，減少延遲問題以及空間問題
#main.set_new_read(True)
_path_obj = oo.path_adder()
path = ["UI","api","jobs","UI/module"]  
for i in path:
    _path_obj.add_path(i)


import h_ui
import h_jobs
import h_Chat


if __name__ == '__main__':
    main.add_threading(h_ui.main,"UI")
    main.add_threading(h_jobs.main,"JOBS" , module_list = ["jobs_updata"])
    main.add_threading(h_Chat.main,"CHAT" , module_list = [])
    if main.start("all"):
        print("[start]>>ok")
        main.run()