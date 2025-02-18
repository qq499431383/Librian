// Generated by CoffeeScript 2.3.2
(function() {
  window.圖像融合 = {
    緩存: {},
    圖像融合: function(圖片名組, f) {
      var go, i, j, len, m, t, 圖片組, 緩存;
      緩存 = this.緩存;
      if (緩存[圖片名組.toString()]) {
        console.log('用緩存');
        t = this.緩存[圖片名組.toString()];
        f(t[0], t[1]);
      }
      m = 0;
      圖片組 = [];
      for (j = 0, len = 圖片名組.length; j < len; j++) {
        i = 圖片名組[j];
        t = new Image();
        t.src = i[0];
        t.setAttribute("crossOrigin", 'Anonymous');
        t.偏移x = i[1];
        t.偏移y = i[2];
        圖片組.push(t);
        t.onload = function() {
          m += 1;
          if (m === 圖片名組.length) {
            return go(緩存);
          }
        };
      }
      return go = function(緩存) {
        var base64, canvas, context, k, len1, 圖片, 極x, 極y;
        console.log(緩存);
        極x = Math.max.apply(Math, (function() {
          var k, len1, results;
          results = [];
          for (k = 0, len1 = 圖片組.length; k < len1; k++) {
            圖片 = 圖片組[k];
            results.push(圖片.width + 圖片.偏移x);
          }
          return results;
        })());
        極y = Math.max.apply(Math, (function() {
          var k, len1, results;
          results = [];
          for (k = 0, len1 = 圖片組.length; k < len1; k++) {
            圖片 = 圖片組[k];
            results.push(圖片.height + 圖片.偏移y);
          }
          return results;
        })());
        console.log(極x, 極y);
        canvas = document.createElement("canvas");
        canvas.width = 極x;
        canvas.height = 極y;
        context = canvas.getContext("2d");
        for (k = 0, len1 = 圖片組.length; k < len1; k++) {
          圖片 = 圖片組[k];
          context.drawImage(圖片, 圖片.偏移x, 圖片.偏移y, 圖片.width, 圖片.height);
        }
        base64 = canvas.toDataURL("image/png");
        緩存[圖片名組.toString()] = [[極x, 極y], base64];
        return f([極x, 極y], base64);
      };
    },
    融合到div: function(圖片名組, 時間, dv) {
      return this.圖像融合(圖片名組, function(尺寸, base64) {
        dv = document.getElementById(dv);
        if (時間 > 0) {
          dv.style.transition = `background ${時間}s, width ${時間}s, height ${時間}s, top ${時間}s, left ${時間}s, transform ${時間}s`;
        } else {
          dv.style.transition = "";
        }
        dv.style.width = 尺寸[0];
        dv.style.height = 尺寸[1];
        return dv.style.backgroundImage = `url(${base64})`;
      });
    }
  };

  // window.onload = ->
//     融合到div([
//         ['體.png', 2, 156],
//         ['0.png', 423, 338],
//     ], 1)

//     document.getElementById('avatar').onclick=->
//         融合到div([
//             ['體.png', 2, 156],
//             ['1.png', 425, 336]
//         ], 0.5)

}).call(this);
