'''
AceProxy configuration script
'''
import logging, platform
from aceclient.acemessages import AceConst

class AceConfig:
  # Ace program key (None uses remote key generator)
  acekey = None
  # Ace Stream Engine host
  acehost = '127.0.0.1'
  # Ace Stream Engine port (autodetect for Windows)
  aceport = 62062
  # Ace Stream age parameter (LT_13, 13_17, 18_24, 25_34, 35_44, 45_54, 55_64, GT_65)
  aceage = AceConst.AGE_18_24
  # Ace Stream sex parameter (MALE or FEMALE)
  acesex = AceConst.SEX_MALE
  # AceClient debug level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
  debug = logging.DEBUG
  
  # HTTP Server host
  httphost = '0.0.0.0'
  # HTTP Server port
  httpport = 8000
  
  # Enable VLC or not
  # I strongly recommend to use VLC, because it lags a lot without it
  # That's Ace Stream Engine fault.
  vlcuse = False
  # VLC host
  vlchost = '127.0.0.1'
  # VLC telnet port
  vlcport = 4212
  # VLC streaming port 
  vlcoutport = 8081
  # VLC password
  vlcpass = 'admin'
  # VLC muxer. You probably want one of this streamable muxers:
  # ts, asf, flv, ogg, mkv
  # You can use ffmpeg muxers too, if your VLC is build with it
  # ffmpeg{mux=NAME} (i.e. ffmpeg{mux=mpegts})
  # 
  # VLC's ts muxer sometimes can work bad, but that's the best choice for now.
  vlcmux = 'ts{use-key-frames}'
  # Force ffmpeg INPUT demuxer in VLC. Sometimes can help.
  vlcforceffmpeg = False
  # VLC debug level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
  vlcdebug = logging.DEBUG
  
  # ------------------------
  # Better not to play with these in non-VLC mode!
  # Set to 0, False, 0 for best performance in VLC mode.
  
  # Stream start delay for dumb players (in seconds)
  videodelay = 2
  # Obey PAUSE and RESUME commands (stops sending data to client, should prevent annoying buffering)
  videoobey = True
  # Stream send delay on PAUSE/RESUME commads (works only if option above is enabled)
  videopausedelay = 3
  # Wait before closing Ace Stream connection when client disconnects
  videodestroydelay = 3
  # Pre-buffering timeout
  videotimeout = 40
  # ------------------------
  
  # Fake User-Agents (not video players) which generates a lot of requests
  # which Ace stream handles badly. Send them 200 OK and do nothing.
  fakeuas = ('Mozilla/5.0 IMC plugin Macintosh', )
  # HTTP debug level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
  httpdebug = logging.DEBUG
  
  
  
  '''
  Do not touch this
  '''
  if platform.system() == 'Windows':
    import _winreg
    import os.path
    reg = _winreg.ConnectRegistry(None, _winreg.HKEY_CURRENT_USER)
    key = _winreg.OpenKey(reg, 'Software\AceStream')
    value = _winreg.QueryValueEx(key, 'EnginePath')
    dirpath = os.path.dirname(value[0])
    try:
      aceport = int(open(dirpath + '\\acestream.port', 'r').read())
    except IOError:
      # Ace Stream is not running, start it
      import subprocess, time
      subprocess.Popen([value[0]])
      _started = False
      for i in xrange(10):
	time.sleep(1)
	try:
	  aceport = int(open(dirpath + '\\acestream.port', 'r').read())
	  _started = True
	  break
	except IOError:
	  _started = False
      if not _started:
	print "Can't start engine!"
	quit()
  '''
  Do not touch this
  '''
