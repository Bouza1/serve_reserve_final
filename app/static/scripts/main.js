export function isMobileDevice() 
{
  // Returns whether the client is a mobile device-
  return(isIOS() || (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)))
}
  
export function isIOS() 
{
  // Returns whether the client is an IOS device, needed because IPAd Bugs
  if (/iPad|iPhone|iPod/.test(navigator.platform)) 
  {
    return true;
  } 
  else 
  {
    return navigator.maxTouchPoints &&
      navigator.maxTouchPoints > 2 &&
      /MacIntel/.test(navigator.platform);
    }
  }

export function set_page_height()
{
  // Sets page layout for desktop devices.
  let page = document.getElementById('whole-page')
  let content_container = document.getElementById('content-container')
  if(isMobileDevice())
  {
  } 
  else 
  {
    page.setAttribute('class', "vh-100 align-items-middle justify-content-center")
  }
}

