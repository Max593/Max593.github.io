(function () {
  // ── Theme toggle ──────────────────────────────────────
  var btn = document.getElementById('theme-toggle');
  if (btn) {
    btn.addEventListener('click', function () {
      var html = document.documentElement;
      var isDark = html.classList.contains('dark');
      html.classList.remove('dark', 'light');
      html.classList.add(isDark ? 'light' : 'dark');
      localStorage.setItem('theme', isDark ? 'light' : 'dark');
    });
  }

  // ── Lightbox for project media ───────────────────────
  var galleryMedia = Array.from(document.querySelectorAll('.project-hero img, .ref-image img, .ref-image video'));
  if (galleryMedia.length) {
    var lightbox = document.createElement('div');
    lightbox.className = 'lightbox';
    lightbox.setAttribute('aria-hidden', 'true');
    lightbox.innerHTML = [
      '<div class="lightbox-dialog" role="dialog" aria-modal="true" aria-label="Expanded project media">',
      '  <button class="lightbox-close" type="button" aria-label="Close media preview">&times;</button>',
      '  <img class="lightbox-image" alt="" hidden>',
      '  <video class="lightbox-video" controls playsinline hidden></video>',
      '  <div class="lightbox-caption"></div>',
      '</div>'
      ,
      '<button class="lightbox-nav lightbox-prev" type="button" aria-label="Previous media" hidden>&lsaquo;</button>',
      '<button class="lightbox-nav lightbox-next" type="button" aria-label="Next media" hidden>&rsaquo;</button>'
    ].join('');
    document.body.appendChild(lightbox);

    var lightboxImage = lightbox.querySelector('.lightbox-image');
    var lightboxVideo = lightbox.querySelector('.lightbox-video');
    var lightboxCaption = lightbox.querySelector('.lightbox-caption');
    var lightboxClose = lightbox.querySelector('.lightbox-close');
    var lightboxPrev = lightbox.querySelector('.lightbox-prev');
    var lightboxNext = lightbox.querySelector('.lightbox-next');
    var currentGroup = [];
    var currentIndex = -1;

    function getMediaCaption(media) {
      if (media.tagName === 'IMG') return media.alt || '';
      var figure = media.closest('.ref-image');
      var caption = figure ? figure.querySelector('figcaption') : null;
      return caption ? caption.textContent : '';
    }

    function getMediaSource(media) {
      if (media.tagName === 'VIDEO') {
        var source = media.querySelector('source');
        return source ? source.src : media.currentSrc || media.src;
      }
      return media.src;
    }

    function getMediaGroup(media) {
      var row = media.closest('.image-row');
      if (!row) return [media];
      return Array.from(row.querySelectorAll('.ref-image img, .ref-image video'));
    }

    function updateNavState() {
      var hasMultiple = currentGroup.length > 1;
      lightboxPrev.hidden = !hasMultiple;
      lightboxNext.hidden = !hasMultiple;
      if (hasMultiple) {
        lightboxPrev.disabled = currentIndex <= 0;
        lightboxNext.disabled = currentIndex >= currentGroup.length - 1;
      }
    }

    function resetLightboxMedia() {
      lightboxImage.hidden = true;
      lightboxImage.removeAttribute('src');
      lightboxImage.alt = '';
      lightboxVideo.pause();
      lightboxVideo.hidden = true;
      lightboxVideo.removeAttribute('src');
      lightboxVideo.load();
    }

    function showMedia(group, index, autoplayVideo) {
      var media = group[index];
      currentGroup = group;
      currentIndex = index;
      resetLightboxMedia();

      if (media.tagName === 'VIDEO') {
        lightboxVideo.src = getMediaSource(media);
        lightboxVideo.hidden = false;
        if (autoplayVideo) {
          var playPromise = lightboxVideo.play();
          if (playPromise && typeof playPromise.catch === 'function') {
            playPromise.catch(function () {});
          }
        }
      } else {
        lightboxImage.src = media.src;
        lightboxImage.alt = media.alt || '';
        lightboxImage.hidden = false;
      }

      lightboxCaption.textContent = getMediaCaption(media);
      updateNavState();
    }

    function closeLightbox() {
      resetLightboxMedia();
      currentGroup = [];
      currentIndex = -1;
      lightbox.classList.remove('is-open');
      lightbox.setAttribute('aria-hidden', 'true');
      document.body.style.overflow = '';
    }

    function navigateLightbox(direction) {
      var nextIndex = currentIndex + direction;
      if (nextIndex < 0 || nextIndex >= currentGroup.length) return;
      showMedia(currentGroup, nextIndex, false);
    }

    galleryMedia.forEach(function (media) {
      media.addEventListener('click', function () {
        var group = getMediaGroup(media);
        var index = group.indexOf(media);
        showMedia(group, index, media.tagName === 'VIDEO');
        lightbox.classList.add('is-open');
        lightbox.setAttribute('aria-hidden', 'false');
        document.body.style.overflow = 'hidden';
      });
    });

    lightboxClose.addEventListener('click', closeLightbox);
    lightboxPrev.addEventListener('click', function () { navigateLightbox(-1); });
    lightboxNext.addEventListener('click', function () { navigateLightbox(1); });
    lightbox.addEventListener('click', function (event) {
      if (event.target.closest('.lightbox-image, .lightbox-video, .lightbox-nav, .lightbox-close')) return;
      closeLightbox();
    });
    document.addEventListener('keydown', function (event) {
      if (!lightbox.classList.contains('is-open')) return;
      if (event.key === 'Escape') closeLightbox();
      if (event.key === 'ArrowLeft') navigateLightbox(-1);
      if (event.key === 'ArrowRight') navigateLightbox(1);
    });
  }

  // ── Ripple wave animation ─────────────────────────────
  var canvas = document.getElementById('ripple-canvas');
  if (!canvas) return;
  var ctx = canvas.getContext('2d');

  var WAVE_COUNT = 7;

  var waves = Array.from({ length: WAVE_COUNT }, function (_, i) {
    return {
      amplitude: 18 + i * 9,
      frequency: 0.003 + i * 0.0008,
      speed: 0.0018 + i * 0.0004,
      phase: (i / WAVE_COUNT) * Math.PI * 2,
      yOffset: 0,
      opacity: 0.045 + (i % 3) * 0.018,
    };
  });

  function isDarkMode() {
    var html = document.documentElement;
    return html.classList.contains('dark') ||
      (!html.classList.contains('light') && window.matchMedia('(prefers-color-scheme: dark)').matches);
  }

  function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    var spacing = canvas.height / (WAVE_COUNT + 1);
    waves.forEach(function (w, i) { w.yOffset = spacing * (i + 1); });
  }

  function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    var w = canvas.width;
    var dark = isDarkMode();
    var rgb = dark ? '201, 168, 122' : '139, 115, 85';
    var opacityBoost = dark ? 2.8 : 1;

    waves.forEach(function (wave) {
      wave.phase += wave.speed;
      ctx.beginPath();
      for (var x = 0; x <= w; x += 4) {
        var y = wave.yOffset
          + Math.sin(x * wave.frequency + wave.phase) * wave.amplitude
          + Math.sin(x * wave.frequency * 0.5 + wave.phase * 0.7) * (wave.amplitude * 0.4);
        if (x === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
      }
      ctx.strokeStyle = 'rgba(' + rgb + ', ' + (wave.opacity * opacityBoost) + ')';
      ctx.lineWidth = 1.5;
      ctx.stroke();
    });

    requestAnimationFrame(draw);
  }

  window.addEventListener('resize', resize);
  resize();
  requestAnimationFrame(draw);
})();
