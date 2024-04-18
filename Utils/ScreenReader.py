import mss
import numpy as np

# Prime numbers are used to get a more random sampling of the image (to avoid sampling the same pixels in a row)
PRIME_NUMBBERS = [1, 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541]

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

    def getAvgScreenColor(self, monitor_num, colorPrecision):
        with mss.mss() as sct:
            sct_img = sct.grab(sct.monitors[monitor_num])

            # Save screenshot to file (commented so disabled)
            # mss.tools.to_png(sct_img.rgb, sct_img.size, output="test.png")

            # mss grabs the pictures as bgra, this code changes it to a RGB array
            frame = np.array(sct_img, dtype=np.uint8)
            rgb_img = np.flip(frame[:, :, :3], 2)

            # Calculating the average color numbers
            avg = np.average(rgb_img[::PRIME_NUMBBERS[colorPrecision]], (0,1))
            return avg