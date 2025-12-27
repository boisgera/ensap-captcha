() => {

  const captcha = document.querySelector('ensap-captcha');
  if (!captcha) return null;

  img = captcha.querySelector('img');

  if (img && img.src) {
    return {
      src: img.src,
      type: 'img'
    };
  }

  // // Check for canvas element
  // const canvas = captcha.shadowRoot?.querySelector('canvas') || captcha.querySelector('canvas');
  // if (canvas) {
  //   return {
  //     src: canvas.toDataURL(),
  //     type: 'canvas'
  //   };
  // }

  // // Check for base64 in any child element
  // const allElements = Array.from(captcha.shadowRoot?.querySelectorAll('*') || captcha.querySelectorAll('*'));
  // for (const el of allElements) {
  //   if (el.src && el.src.startsWith('data:image')) {
  //     return {
  //       src: el.src,
  //       type: 'data'
  //     };
  //   }
  // }

  // return null;
}