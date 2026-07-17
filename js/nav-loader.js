/**
 * Navigation, Header, and Footer Loader
 * Loads shared navigation, header, and footer using innerHTML (works with file:// protocol)
 */

(function() {
	// Detect if we're in a subdirectory (like blog/)
	var pathPrefix = '';
	var currentPath = window.location.pathname;

	// Check if we're in a subdirectory
	if (currentPath.includes('/blog/') || currentPath.match(/\/blog\/[^\/]+\.html$/) || currentPath.includes('/interests/') || currentPath.includes('/math-and-cs/')) {
		pathPrefix = '../';
	}

	// ---- Shared preferences (dark/light theme + zoom level) via a cookie, so
	// every page on the site opens with the same look the visitor last chose. ----
	function setCookie(k, v) { try { document.cookie = k + '=' + encodeURIComponent(v) + ';path=/;max-age=31536000;samesite=lax'; } catch (e) {} }
	function getCookie(k) { var m = document.cookie.match('(?:^|; )' + k + '=([^;]*)'); return m ? decodeURIComponent(m[1]) : null; }
	function ls(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
	function applySavedPrefs() {
		var t = getCookie('theme') || ls('theme') || 'dark';
		document.documentElement.setAttribute('data-theme', t);
		try { localStorage.setItem('theme', t); } catch (e) {}
		setCookie('theme', t);
	}
	applySavedPrefs();

	// Blog posts data (sorted by date, newest first)
	var blogPosts = [
		{
			filename: '2025_11_12_16_week_olympic_triathlon_training_plan.html',
			title: '16 Week Olympic Triathlon Training Plan'
		},
		{
			filename: '2022_12_12_so_you_want_to_animate_your_pdf_files.html',
			title: 'So you want to animate your PDF files?'
		}
	];

	// Helper function to truncate title for display
	function truncateTitle(title, maxLength) {
		if (title.length <= maxLength) {
			return title;
		}
		return title.substring(0, maxLength) + '...';
	}

	// Header HTML template
	var headerHTML = `<div class="header-content">
	<h1 class="myTitle">KEIVAN MONFARED</h1>
	<p class="myTitleFooter">Mathematician | Data Scientist | Communicator</p>
</div>`;

	// Navigation HTML template with dynamic path prefix
	var navHTML = `<nav id="stickThis">
	<div id="menu">
		<a href="${pathPrefix}index.html">home</a>
		<a href="${pathPrefix}projects.html">projects</a>
		<a href="${pathPrefix}notes.html">notes</a>
		<a href="${pathPrefix}interests.html">interests</a>
		<a href="${pathPrefix}about.html">about</a>
	</div>
	<div id="small_menu">
		<!-- Page-specific sub-menu will be inserted here by each page -->
	</div>
</nav>`;

	// Footer HTML template
	var footerHTML = `<div class="social-media">
	<a href="http://www.github.com/k1monfared" target="_blank" aria-label="GitHub" class="social-icon social-github"></a>
	<a href="http://www.linkedin.com/in/k1monfared" target="_blank" aria-label="LinkedIn" class="social-icon social-linkedin"></a>
	<a href="http://scholar.google.com/citations?hl=en&user=usBmFlsAAAAJ" target="_blank" aria-label="Google Scholar" class="social-icon social-scholar"></a>
	<a href="https://arxiv.org/search/?searchtype=author&query=Monfared%2C+K" target="_blank" aria-label="arXiv" class="social-icon social-arxiv"></a>
	<a href="${pathPrefix}sponsor.html" aria-label="Support my work" title="Support my work" class="social-icon social-sponsor"></a>
</div>`;

	// Load header
	function loadHeader() {
		var headerContainer = document.querySelector('.site-header');
		if (headerContainer) {
			headerContainer.innerHTML = headerHTML;
		}
	}

	// Load navigation
	function loadNavigation() {
		var navContainer = document.getElementById('nav-container');
		if (navContainer) {
			navContainer.innerHTML = navHTML;
			// After nav loads, set the active page
			setActivePage();
			// Load blog post navigation if we're in a blog post
			loadBlogPostNavigation();
			// Re-initialize sticky functionality
			initializeStickyNav();
			// Dispatch event so page-specific scripts can populate small_menu
			window.dispatchEvent(new Event('navigationLoaded'));
		}
	}

	// Load blog post navigation (prev/current/next)
	function loadBlogPostNavigation() {
		var currentPath = window.location.pathname;
		var currentPage = currentPath.split('/').pop();

		// Check if we're in a blog post (not blog.html itself)
		var inBlogPost = currentPath.includes('/blog/') && currentPage !== 'blog.html';

		if (!inBlogPost) {
			return; // Not in a blog post, don't show navigation
		}

		// Find current post index
		var currentIndex = -1;
		for (var i = 0; i < blogPosts.length; i++) {
			if (blogPosts[i].filename === currentPage) {
				currentIndex = i;
				break;
			}
		}

		if (currentIndex === -1) {
			return; // Current post not found in blogPosts array
		}

		// Get previous and next posts
		var prevPost = currentIndex < blogPosts.length - 1 ? blogPosts[currentIndex + 1] : null;
		var nextPost = currentIndex > 0 ? blogPosts[currentIndex - 1] : null;
		var currentPost = blogPosts[currentIndex];

		// Build navigation HTML - simple text links like other subnavs
		var blogNavHTML = '';

		// Previous link
		if (prevPost) {
			blogNavHTML += '<a href="' + prevPost.filename + '" title="' + prevPost.title + '">&lt;&lt;</a>';
		} else {
			blogNavHTML += '<span class="disabled">&lt;&lt;</span>';
		}

		// Current post title (truncated to 40 characters)
		blogNavHTML += '<span class="current-post">' + truncateTitle(currentPost.title, 40) + '</span>';

		// Next link
		if (nextPost) {
			blogNavHTML += '<a href="' + nextPost.filename + '" title="' + nextPost.title + '">&gt;&gt;</a>';
		} else {
			blogNavHTML += '<span class="disabled">&gt;&gt;</span>';
		}

		// Insert into small_menu
		var smallMenu = document.getElementById('small_menu');
		if (smallMenu) {
			smallMenu.innerHTML = blogNavHTML;
		}
	}

	// Load footer
	function loadFooter() {
		var footerContainer = document.getElementById('footer-container');
		if (footerContainer) {
			footerContainer.innerHTML = footerHTML;
		}
	}

	// Create theme toggle button and wire up its click handler.
	// site_kit theme.js runs its DOMContentLoaded listener before this one
	// (it's loaded first in the head), so its own click-handler attach misses
	// the button. We attach our own here.
	function createThemeToggleButton() {
		if (document.getElementById('theme-toggle')) return;
		var btn = document.createElement('button');
		btn.id = 'theme-toggle';
		btn.setAttribute('aria-label', 'Toggle theme');
		document.body.appendChild(btn);

		btn.addEventListener('click', function () {
			var current = document.documentElement.getAttribute('data-theme') || 'dark';
			var next = current === 'dark' ? 'light' : 'dark';
			document.documentElement.setAttribute('data-theme', next);
			try { localStorage.setItem('theme', next); } catch (e) {}
			setCookie('theme', next);
		});
	}

	// Set active page based on current URL
	function setActivePage() {
		// Get current page filename
		var currentPath = window.location.pathname;
		var currentPage = currentPath.split('/').pop();

		// If no page specified (directory), assume index.html
		if (currentPage === '' || currentPage === '/') {
			currentPage = 'index.html';
		}

		// Check if we're in a blog post (in blog subdirectory but not blog.html)
		var inBlogPost = currentPath.includes('/blog/') && currentPage !== 'blog.html';
		var inInterestPage = currentPath.includes('/interests/');
		var inMathAndCsPage = currentPath.includes('/math-and-cs/');

		// Find the menu links that match current page
		var menuLinks = document.querySelectorAll('#menu a');
		menuLinks.forEach(function(link) {
			var href = link.getAttribute('href');
			var linkPage = href.split('/').pop(); // Get filename without path prefix

			// Match exact page, blog section, interests section, or math-and-cs section
			if (linkPage === currentPage || (inBlogPost && linkPage === 'blog.html') || (inInterestPage && linkPage === 'interests.html') || (inMathAndCsPage && linkPage === 'math-and-cs.html')) {
				// Mark this link as active
				link.classList.add('active');
			}
		});
	}

	// Initialize sticky navigation functionality
	function initializeStickyNav() {
		function sticktothetop() {
			var window_top = window.pageYOffset || document.documentElement.scrollTop;
			var stickHere = document.getElementById('stick-here');

			if (stickHere) {
				var top = stickHere.offsetTop;
				var stickThis = document.getElementById('stickThis');

				if (window_top > top) {
					stickThis.classList.add('stick');
					stickHere.style.height = stickThis.offsetHeight + 'px';
				} else {
					stickThis.classList.remove('stick');
					stickHere.style.height = '0';
				}
			}
		}

		// Attach scroll handler
		window.addEventListener('scroll', sticktothetop);
		sticktothetop();
	}

	// Initialize when document is ready
	if (document.readyState === 'loading') {
		document.addEventListener('DOMContentLoaded', function() {
			loadHeader();
			loadNavigation();
			loadFooter();
			createThemeToggleButton();
		});
	} else {
		loadHeader();
		loadNavigation();
		loadFooter();
		createThemeToggleButton();
	}
})();
