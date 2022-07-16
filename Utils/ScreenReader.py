import mss
import numpy as np

class ScreenReader:
    def getScreensList(self):
        # Getting screens for GUI dropdownlist
        with mss.mss() as sct:
            print('Reading Screens:')

            # 0 - All monitors
            # 1 - Display 1
            # 2 - Display 2
            # And so on
            screens_list = sct.monitors # For further development: sct.monitors contains more interesting data

            for i in range(len(screens_list)): # iterating on screens by indexes
                print(screens_list[i])
                screens_list[i] = i

            screens_list[0] = "All" # Changing name for UX

            return screens_list

    def getAvgScreenColor(self, monitor_num):
        with mss.mss() as sct:
            sct_img = sct.grab(sct.monitors[monitor_num])

            # Save screenshot to file (commented so disabled)
            # mss.tools.to_png(sct_img.rgb, sct_img.size, output="test.png")

            # mss grabs the pictures as bgra, this code changes it to a RGB array
            frame = np.array(sct_img, dtype=np.uint8)
            rgb_img = np.flip(frame[:, :, :3], 2)

            # Calculating the average color numbers
            avg = np.average(rgb_img, (0,1))
            return avg