/**
 * Navigation and Footer Loader
 * Loads shared navigation and footer, and sets active page state
 */

(function() {
	// Load navigation using fetch
	function loadNavigation() {
		fetch('nav.html')
			.then(response => {
				if (!response.ok) throw new Error('Nav load failed');
				return response.text();
			})
			.then(html => {
				document.getElementById('nav-container').innerHTML = html;
				// After nav loads, set the active page
				setActivePage();
				// Re-initialize sticky functionality
				initializeStickyNav();
				// Dispatch event so page-specific scripts can populate small_menu
				window.dispatchEvent(new Event('navigationLoaded'));
			})
			.catch(error => {
				console.error('Error loading navigation:', error);
				// Fallback: show error or load inline
			});
	}

	// Load footer using fetch
	function loadFooter() {
		fetch('footer.html')
			.then(response => {
				if (!response.ok) throw new Error('Footer load failed');
				return response.text();
			})
			.then(html => {
				document.getElementById('footer-container').innerHTML = html;
			})
			.catch(error => {
				console.error('Error loading footer:', error);
			});
	}

	// Set active page based on current URL
	function setActivePage() {
		// Get current page filename
		var currentPage = window.location.pathname.split('/').pop();

		// If no page specified (directory), assume index.html
		if (currentPage === '' || currentPage === '/') {
			currentPage = 'index.html';
		}

		// Find the menu item that matches current page
		var menuItems = document.querySelectorAll('#menu .menuItem');
		menuItems.forEach(function(item) {
			var link = item.querySelector('a');
			var href = link.getAttribute('href');

			if (href === currentPage) {
				// Mark this item as active
				item.setAttribute('id', 'this_page');
				link.style.color = '#FFD700';
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
			loadNavigation();
			loadFooter();
		});
	} else {
		loadNavigation();
		loadFooter();
	}
})();
