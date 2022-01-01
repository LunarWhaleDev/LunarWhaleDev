import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler

token = ""

vtext = (
  "Pools and contents at snapshot used for calculations:\n\n"
  "LAVA-PYR Pool\n"
  "LP Tokens: 46,181.53\n"
  "LAVA: 528,105.58\n"
  "PYR: 4,193.82\n\n"
  "USDC-PYR Pool\n"
  "LP Tokens: .00904978\n"
  "USDC: 42,028.79\n"
  "PYR: 2,253.97\n\n"
  "WETH-PYR Pool\n"
  "LP Tokens: 113.18\n"
  "WETH: 8.22\n"
  "PYR: 1,748.34\n\n"
  "MATIC-PYR Pool\n"
  "LP Tokens: 11,589.67\n"
  "MATIC: 33,369.57\n"
  "PYR: 4,586.51\n\n"
  )

#pyr value per LP. usdc looks funny because it was always issued decimal values. decimal place isnt relevant tho, underlying value is same for everyone.

lavapyr = .18162
usdcpyr = 498127
wethpyr = 30.895
maticpyr = .79148

snap = {
  "0x1c1a7507c00c8798b5e6a62a96c91885f31170a7": [1533.540753, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "0x3221c24f7898117578435a4968a11759b8dfcb3f": [116.7978497, 85.25167102, 0, 0, 0, 0, 2300, 0, 0, 0, 0, 686, 0, 0],
  "0x38f25ad6524824f0c6f45f31e000d99938f01bf9": [1.416687856, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "0x4d334060aa328d8471ff791b54cf46f128427879": [62.39557738, 0, 0, 0, 0, 0, 0, 0, 0, 3000, 0, 0, 0, 0],
  "0x53ffafdd7e3e21f94fb39b2401d0db9c8817f643": [510.5383476, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "0x5a685e4547d99a95ca854861749e1c792ee5b864": [91.77750403, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2000],
  "0x6257d899cc16cdcba3218fa065dca6c42aef3d2c": [74.84901596, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "0x65dfd653afef0bfd337c3e9a85cc16a274ef0652": [1673.487176, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "0x6a61c72037cbad9d2b56976ea4ff7f17969af4ca": [14.12920322, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "0x748144ce397f93991115ffb94fca6ff2f4747b81": [371.5017226, 0, 0, 0, 280, 0, 0, 530, 0, 0, 0, 0, 0, 2000],
  "0x7526c41c57e8474f5351434cd0e54e023b438b4a": [0.5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "0x76fbd4ad2dc56494cd4df33ec73a68dff268725f": [25.96678005, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "0x80d2830ab9b174f497b5b064d3d56f94fddbbaf7": [84.76772669, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "0x9764fad008799c95c824caf4ff2fb55bb372c0c4": [77.97584707, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "0x9f05bff2a45b7dd944efc6ce987636e8adbf0898": [3807.163532, 0, 0.0005488815384, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "0xa072f8e1e5d10ae49d59f80b4f50e54616d5c290": [32.81873901, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "0xa14ccec08153a65c24dfb25e04a3f5f241401aee": [11.86707901, 0.7308609562, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "0xa3b353e5488633c8c10b494da67b05991a03df8a": [917.1724883, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "0xa86de87c454623a848fe12c24bc449fd16f371bf": [55.66536064, 4.369034678, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "0xdd60a7ec4c0ed26b5fcea008572b3f834a8a6265": [23.52525981, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "0xeb8403366443ff0ec62c93ed88cb12fb01d4be76": [761.9316956, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2000],
  "0xf5a69115739b529a7b3145c8d03a3941c5e454d3": [116.0087563, 29.94646091, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "0xfb71f16297d717ad28ee0a97a6996b9d5082b625": [15.73511323, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "0xfe0e493564db7ae23a7b6ea07f2c633ee8f25f22": [2000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "0x08b73ec14f2518de3ce0c3cb2ba3f6623a465329": [0, 0.002369460571, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "0x0df302040534c94ada50f1bd0c68b0b765b3037c": [0, 76.05748916, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "0x10ddc2e7f1f83bc7d2c83c07322eb9c2ec39fd31": [0, 54.79161035, 0, 0, 0, 0, 0, 0, 0, 0, 0, 343, 0, 0],
  "0x132ad17779eaca2810da92a77c0936ea5db20fc0": [0, 13.67317313, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "0x1598d1346412288428363e618aa0b2f27f550a44": [0, 0.03613990642, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "0x1f5343f93801bc28c00c75f9f54a588c32918e6a": [0, 43.91904814, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "0x2101085bd34236fbdd923262d2065c89a873a5ea": [0, 0.5448356174, 0, 0.4628380781, 0, 24, 0, 0, 0, 0, 0, 343, 0, 0],
  "0x26a3d999a92cddf8257b9d50860d418bbd8fb1f0": [0, 3.966589267, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "0x3c8b06f16e421dc72aea2584a75f912ad36e6be0": [0, 68.43298752, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "0x40601f4fd4b21718d12223df35c9598a4982ec4e": [0, 357.9849917, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "0x41c0ddfaa0bae0b049ba18d58d51ec2f6bb4c9cb": [0, 2.00E-18, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "0x41e3a87a83a97feef756695ef8c066ecca75a54d": [0, 10.29483992, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "0x4cc21b26e6bee8764ad2a63fd829724a113e87dd": [0, 0.04025658788, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "0x5e33d191802b10f9a1eaed452263198888344df7": [0, 0.4119078036, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "0x627e46f5922b5601ada533cb229c519103537c28": [0, 27.68398771, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "0x63849e29bea95875040895761077d4309c33b909": [0, 13.53931699, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "0x71321307d423dfa3504888211848460c24bffd60": [0, 20.75580385, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "0x830cbe050ad3de8722e32040c4664ea40179712c": [0, 2.221880994, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "0x9449d6dc1034f8b06c507ca5d640f907826f06db": [0, 0.02497268224, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "0x9ec06d09509658ff215c6d0e193a958196848327": [0, 106.240854, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "0x9ef5d5b965b6b2bd05123e9500bb54d523e701c0": [0, 0.006107647614, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "0xa405bb5b1cea47eb4e456cfe82923688bc4acf84": [0, 1467.978742, 0, 0, 0, 0, 0, 530, 0, 0, 0, 0, 0, 0],
  "0xacff55cdf272370544c64dbf72a5de263b15b8b0": [0, 1660.416617, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "0xb3cc3dcc48e1b825b4628e9384829d04536c7b5f": [0, 1.00E-18, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "0xb97512961ced4b61658f869e5931ce223795bb87": [0, 2.173798242, 0, 0, 280, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "0xbb461f20b26ee778c7d28485d4cbe489738f2a4a": [0, 1.00E-17, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "0xbf88a5068dd0fa84f309e76d30dd624f52422614": [0, 138.2789353, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "0xc5ee54238e88b5deed1ce065279b0edaa566dace": [0, 0.5986332268, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "0xc6950edabbda7476654a6071f39778e8ce2922be": [0, 321.3260951, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "0xc6ee2f969c83b7a8d6f0fb3a540b8f92e95d31f2": [0, 4.700731686, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "0xdc99e9372f07cac7df165a95825e6f224fd51d9f": [0, 0.0250168642, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "0xe4aef19865b63329a851c184585a9cfe981d7bd7": [0, 24.95785056, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "0xe935430b53e0187b77479daebfba956c199c8f67": [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "0xeb9dd2177906b7679e3854364df6c997419069b3": [0, 212.2698891, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "0xf401fcde41d0e04f3c553e42961a87a44e713543": [0, 1.090666264, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "0xf5d9d607d0275d8096c27bc9c6d93a50ba7228f7": [0, 102.5921878, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "0xfd1ab0f336224104e9a66b2e07866241a87c96fc": [0, 0.3342524608, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "0xb658bb1428956c183c5def6aaa0fe2c1a3f2bf92": [0, 0, 0.0008, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "0xc814b982c867358fa58e0c8357d2819075d11296": [0, 0, 8.99E-07, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "0x8addabf339c54aa0c6e8adb41c2cb2f1d68451f5": [0, 0, 0, 8.477658537, 0, 12, 0, 0, 0, 0, 0, 0, 0, 0],
  "0xc955a94a9008783ce147d0d104a3344389680a19": [0, 0, 0, 12, 0, 0, 0, 530, 0, 0, 0, 0, 0, 0],
  "0xd8d38f9a38397d7613b2ad79661894a715133964": [0, 0, 0, 3.312381235, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "0xe348e4dc220698453496e82415ab2a2417d298e3": [0, 0, 0, 0.3410141175, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "0xf669be3593640a69dad91eb4dce16970071c4f34": [0, 0, 0, 0.2694265576, 0, 0, 0, 0, 0, 0, 0, 0, 5.13, 0],
  "0x688576371e9e54186658db78172d5b403f811824": [0, 0, 0, 0, 280, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "0x925304029c80aa94d1d5f274ef640cd49f58cfc6": [0, 0, 0, 0, 280, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "0xeb2c1228997f159f505dd769291b1b9bbe398e1a": [0, 0, 0, 0, 280, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "0xd8df5790ac4bde5bb406ea8ad582ee2184aa9ab0": [0, 0, 0, 0, 280, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "0x8d0e3f6007d3d9674d01daf57a4d135887350a34": [0, 0, 0, 0, 0, 12, 0, 530, 7.8, 1500, 0.00055, 343, 5.13, 2000],
  "0x45daf121b6d5bad5e77ec2c3a5828209286e66e6": [0, 0, 0, 0, 0, 0, 2300, 0, 0, 0, 0, 0, 0, 0],
  "0x907d3fa20cdd3b6db970592f97419abbcf2179ea": [0, 0, 0, 0, 0, 0, 4600, 0, 0, 0, 0, 0, 0, 0],
  "0x4e98a6a5c8575b7bf31124b38b975b2f0af34b22": [0, 0, 0, 0, 0, 0, 2300, 0, 0, 0, 0.00715, 0, 0, 0],
  "0x0384c61f4fab97f8c2db5943b96dbbc9f1371ebb": [0, 0, 0, 0, 0, 0, 2300, 0, 0, 0, 0, 0, 0, 0],
  "0x3338c76de340a8b827fef249a401cecd0ed95883": [0, 0, 0, 0, 0, 0, 0, 530, 0, 0, 0, 0, 0, 0],
  "0xfc14306d7b7a84345b4d7645c29ee895bdea887b": [0, 0, 0, 0, 0, 0, 0, 0, 0, 1500, 0, 0, 0, 0],
  "0x636ea54c11be0b07816b636c7984f757dccf1e9e": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 343, 0, 0],
  "0xd4121ec838e91b941355daec42ed96d6e72cd81d": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 343, 0, 0],
  "0xcc345010f08390f95e418293835491405ab25f97": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5.13, 2000],
  "0x35fde1ff8b8afbab9fb071f73b9114d91a4c1d28": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5.13, 0],
  "0xfa949ce340ef6ea03c94002543e01f33e0920f62": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2000],
  "0x931e676e543f80b84f6874d182ade7130178ae05": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2000]
  }

def snapshot(update, context):
  if not context.args:
    update.effective_chat.send_message("Please include your address.\nExample '/snapshot 0xYourAddressLettersAndNumbers'")
    return
  address = context.args[0].lower()
  if address not in snap:
    update.effective_chat.send_message("Address not in snapshot")
    return
  newpyr = 0
  text = "Your LP Tokens in Snapshot:\n\n"
  l = snap[address]
  if l[0] > 0:
    text = (
      f"{text}LAVA-PYR LP in Wallet:\n"
      f"{l[0]}\n"
      f"={l[0] * lavapyr} PYR\n\n"
      )
    newpyr = newpyr + (l[0] * lavapyr)
  if l[1] > 0:
    text = (
      f"{text}MATIC-PYR LP in Wallet:\n"
      f"{l[1]}\n"
      f"={l[1] * maticpyr} PYR\n\n"
      )
    newpyr = newpyr + (l[1] * maticpyr)
  if l[2] > 0:
    text = (
      f"{text}USDC-PYR LP in Wallet:\n"
      f"{l[2]}\n"
      f"={l[2] * usdcpyr} PYR\n\n"
      )
    newpyr = newpyr + (l[2] * usdcpyr)
  if l[3] > 0:
    text = (
      f"{text}WETH-PYR LP in Wallet:\n"
      f"{l[3]}\n"
      f"={l[3] * wethpyr} PYR\n\n"
      )
    newpyr = newpyr + (l[3] * wethpyr)
  if l[4] > 0:
    text = (
      f"{text}MATIC-PYR LP in Pipes of Pan Farm:\n"
      f"{l[4]}\n"
      f"={l[4] * maticpyr} PYR\n\n"
      )
    newpyr = newpyr + (l[4] * maticpyr)
  if l[5] > 0:
    text = (
      f"{text}WETH-PYR LP in Orange Tunic Farm:\n"
      f"{l[5]}\n"
      f"={l[5] * wethpyr} PYR\n\n"
      )
    newpyr = newpyr + (l[5] * wethpyr)
  if l[6] > 0:
    text = (
      f"{text}LAVA-PYR LP in Olive Tunic Farm:\n"
      f"{l[6]}\n"
      f"={l[6] * lavapyr} PYR\n\n"
      )
    newpyr = newpyr + (l[6] * lavapyr)
  if l[7] > 0:
    text = (
      f"{text}MATIC-PYR LP in Notus Rod Farm:\n"
      f"{l[7]}\n"
      f"={l[7] * maticpyr} PYR\n\n"
      )
    newpyr = newpyr + (l[7] * maticpyr)
  if l[8] > 0:
    text = (
      f"{text}WETH-PYR LP in Boreas Rod Farm:\n"
      f"{l[8]}\n"
      f"={l[8] * wethpyr} PYR\n\n"
      )
    newpyr = newpyr + (l[8] * wethpyr)
  if l[9] > 0:
    text = (
      f"{text}LAVA-PYR LP in Hades Flag Farm:\n"
      f"{l[9]}\n"
      f"={l[9] * lavapyr} PYR\n\n"
      )
    newpyr = newpyr + (l[9] * lavapyr)
  if l[10] > 0:
    text = (
      f"{text}USDC-PYR LP in Arcadia Flag Farm:\n"
      f"{l[10]}\n"
      f"={l[10] * usdcpyr} PYR\n\n"
      )
    newpyr = newpyr + (l[10] * usdcpyr)
  if l[11] > 0:
    text = (
      f"{text}MATIC-PYR LP in Boreas Flag Farm:\n"
      f"{l[11]}\n"
      f"={l[11] * maticpyr} PYR\n\n"
      )
    newpyr = newpyr + (l[11] * maticpyr)
  if l[12] > 0:
    text = (
      f"{text}WETH-PYR LP in Notus Flag Farm:\n"
      f"{l[12]}\n"
      f"={l[12] * wethpyr} PYR\n\n"
      )
    newpyr = newpyr + (l[0] * wethpyr)
  if l[13] > 0:
    text = (
      f"{text}LAVA-PYR LP in War Banners Farm:\n"
      f"{l[13]}\n"
      f"={l[13] * lavapyr} PYR\n\n"
      )
    newpyr = newpyr + (l[13] * lavapyr)

  update.effective_chat.send_message(vtext)
  update.effective_chat.send_message(text)
  update.effective_chat.send_message(f"New PYR Value: {newpyr}")

def main():
    updater = Updater(token=token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("snapshot", snapshot))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
