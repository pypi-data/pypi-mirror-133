export function pixiKey(value) {
  const key = {};
  key.value = value;
  key.isDown = false;
  key.isUp = true;
  key.press = null;
  key.release = null;

  let downListener = null;
  let upListener = null;

  key.downHandler = (event) => {
    if (event.key === key.value) {
      if (key.isUp && key.press) {
        key.press();
      }
      key.isDown = true;
      key.isUp = false;
      event.preventDefault();
      window.addEventListener('keyup', upListener, false);
      window.removeEventListener('keydown', downListener);
    }
  };

  key.upHandler = (event) => {
    if (event.key === key.value) {
      if (key.isDown && key.release) {
        key.release();
      }
      key.isDown = false;
      key.isUp = true;
      event.preventDefault();
      window.addEventListener('keydown', downListener, false);
      window.removeEventListener('keyup', upListener);
    }
  };

  downListener = key.downHandler.bind(key);
  upListener = key.upHandler.bind(key);

  window.addEventListener('keydown', downListener, false);

  // Detach event listeners
  key.destroy = () => {
    window.removeEventListener('keydown', downListener);
    window.removeEventListener('keyup', upListener);
  };

  return key;
}
