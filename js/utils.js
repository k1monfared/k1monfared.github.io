/**
 * Vanilla JS utilities — template renderers & toggle
 */

// Monochrome SVG icons (stroke-based, 16x16)
var ICONS = {
	pdf:       '<svg viewBox="0 0 16 16"><path d="M4 1h6l4 4v10H2V1z"/><path d="M10 1v4h4"/></svg>',
	arxiv:     '<svg viewBox="0 0 16 16"><path d="M3 13L13 3M13 3H7M13 3v6"/></svg>',
	abstract:  '<svg viewBox="0 0 16 16"><path d="M3 4h10M3 7h10M3 10h6"/></svg>',
	takeaways: '<svg viewBox="0 0 16 16"><path d="M8 1.5a3.5 3.5 0 012 6.35V10H6V7.85A3.5 3.5 0 018 1.5z"/><path d="M6 11.5h4M6.5 13h3"/></svg>',
	code:      '<svg viewBox="0 0 16 16"><path d="M5 4L1 8l4 4M11 4l4 4-4 4"/></svg>',
	paper:     '<svg viewBox="0 0 16 16"><path d="M4 1h6l4 4v10H2V1z"/><path d="M10 1v4h4"/><path d="M5 7h6M5 9.5h4"/></svg>',
	talk:      '<svg viewBox="0 0 16 16"><path d="M2 3h12v8H9l-3 3v-3H2z"/></svg>',
	link:      '<svg viewBox="0 0 16 16"><path d="M6.5 9.5l3-3M7 5.5L9.5 3a2.12 2.12 0 013 3L10 8.5M9 10.5L6.5 13a2.12 2.12 0 01-3-3L6 7.5"/></svg>',
	thesis:    '<svg viewBox="0 0 16 16"><path d="M8 1L1 4l7 3 7-3-7-3z"/><path d="M3 5.5v5l5 2.5 5-2.5v-5"/></svg>'
};

/**
 * Render paper/patent items.
 *
 * Fields: title, url, tag, pdfUrl, arxivUrl, thumb, authors, abstract,
 *         takeaways, codeUrl, codeLabel
 */
function renderPapers(containerId, papers, defaultThumb) {
	var ul = document.getElementById(containerId);
	if (!ul) return;

	papers.forEach(function(p, i) {
		var li = document.createElement('li');
		var id = containerId + '-' + i;
		li.className = 'paper-item';

		var thumbSrc = p.thumb || defaultThumb;
		var hasThumb = !!thumbSrc;
		var hasDetails = p.authors || p.abstract;
		var icon = hasThumb
			? '<img class="paper-thumb" src="' + thumbSrc + '" alt="">'
			: '<span class="paper-icon paper-icon-lg">' + ICONS.paper + '</span>';

		// Line 1: title
		var titleHtml = p.url
			? '<a href="' + p.url + '" target="_blank">' + p.title + '</a>'
			: '<span class="paper-title-text">' + p.title + '</span>';

		// Line 2: authors (always visible)
		var authorsHtml = p.authors ? '<div class="paper-authors">' + p.authors + '</div>' : '';

		// Line 3: meta row
		var meta = '<div class="paper-meta">';
		if (p.tag) meta += '<span class="paper-venue">' + p.tag + '</span>';
		if (p.pdfUrl) meta += '<a class="paper-action-btn" href="' + p.pdfUrl + '" target="_blank">' + ICONS.pdf + 'PDF</a>';
		if (p.arxivUrl) meta += '<a class="paper-action-btn" href="' + p.arxivUrl + '" target="_blank">' + ICONS.arxiv + 'arXiv</a>';
		if (p.abstract) meta += '<button class="paper-action-btn" onclick="toggleSlowly(\'' + id + '-abs\')">' + ICONS.abstract + 'Abstract</button>';
		if (p.takeaways) meta += '<button class="paper-action-btn" onclick="toggleSlowly(\'' + id + '-tk\')">' + ICONS.takeaways + 'Takeaways</button>';
		if (p.codeUrl) meta += '<a class="paper-action-btn" href="' + p.codeUrl + '" target="_blank">' + ICONS.code + (p.codeLabel || 'Code') + '</a>';
		meta += '</div>';

		var header = '<div class="paper-header">' + icon +
			'<div class="paper-info">' + titleHtml + authorsHtml + meta + '</div></div>';

		// Expandable details
		var detailPad = hasThumb ? '' : ' style="padding-left: calc(44px + 0.75rem);"';
		var details = '';
		if (p.abstract) {
			details += '<div id="' + id + '-abs" class="collapsible paper-details"' + detailPad + '>';
			details += '<p>' + p.abstract + '</p>';
			details += '</div>';
		}
		if (p.takeaways) {
			details += '<div id="' + id + '-tk" class="collapsible paper-details"' + detailPad + '>';
			details += '<p>' + p.takeaways + '</p>';
			details += '</div>';
		}

		li.innerHTML = header + details;
		ul.appendChild(li);
	});

	_retypeset(ul);
}

/**
 * Render talk items.
 * Fields: title, url, venue, year, location, slidesUrl, abstractUrl, videoUrl
 */
function renderTalks(containerId, talks, defaultThumb) {
	var ul = document.getElementById(containerId);
	if (!ul) return;

	talks.forEach(function(t) {
		var li = document.createElement('li');
		li.className = 'paper-item';

		var thumbSrc = t.thumb || defaultThumb;
		var icon = thumbSrc
			? '<img class="paper-thumb" src="' + thumbSrc + '" alt="">'
			: '<span class="paper-icon paper-icon-lg">' + ICONS.talk + '</span>';

		var titleHtml = t.url
			? '<a href="' + t.url + '" target="_blank">' + t.title + '</a>'
			: '<span class="paper-title-text">' + t.title + '</span>';

		var meta = '<div class="paper-meta">';
		if (t.venue) meta += '<span class="paper-venue">' + t.venue + '</span>';
		if (t.year) meta += '<span class="paper-venue">' + t.year + '</span>';
		if (t.location) meta += '<span class="paper-venue">' + t.location + '</span>';
		if (t.slidesUrl) meta += '<a class="paper-action-btn" href="' + t.slidesUrl + '" target="_blank">' + ICONS.pdf + 'Slides</a>';
		if (t.abstractUrl) meta += '<a class="paper-action-btn" href="' + t.abstractUrl + '" target="_blank">' + ICONS.link + 'Abstract</a>';
		if (t.videoUrl) meta += '<a class="paper-action-btn" href="' + t.videoUrl + '" target="_blank">' + ICONS.link + 'Video</a>';
		meta += '</div>';

		li.innerHTML = '<div class="paper-header">' + icon +
			'<div class="paper-info">' + titleHtml + meta + '</div></div>';

		ul.appendChild(li);
	});
}

/**
 * Render thesis items.
 * Fields: title, url, degree, institution, year
 */
function renderTheses(containerId, theses, defaultThumb) {
	var ul = document.getElementById(containerId);
	if (!ul) return;

	theses.forEach(function(t) {
		var li = document.createElement('li');
		li.className = 'paper-item';

		var thumbSrc = t.thumb || defaultThumb;
		var icon = thumbSrc
			? '<img class="paper-thumb" src="' + thumbSrc + '" alt="">'
			: '<span class="paper-icon paper-icon-lg">' + ICONS.thesis + '</span>';

		var titleHtml = t.url
			? '<a href="' + t.url + '" target="_blank">' + t.title + '</a>'
			: '<span class="paper-title-text">' + t.title + '</span>';

		var meta = '<div class="paper-meta">';
		if (t.degree) meta += '<span class="paper-venue">' + t.degree + '</span>';
		if (t.institution) meta += '<span class="paper-venue">' + t.institution + '</span>';
		if (t.year) meta += '<span class="paper-venue">' + t.year + '</span>';
		meta += '</div>';

		li.innerHTML = '<div class="paper-header">' + icon +
			'<div class="paper-info">' + titleHtml + meta + '</div></div>';

		ul.appendChild(li);
	});
}

/**
 * Render code/tool items.
 * Fields: title, url, description
 */
function renderCode(containerId, items, defaultThumb) {
	var ul = document.getElementById(containerId);
	if (!ul) return;

	items.forEach(function(c) {
		var li = document.createElement('li');
		li.className = 'paper-item';

		var thumbSrc = c.thumb || defaultThumb;
		var icon = thumbSrc
			? '<img class="paper-thumb" src="' + thumbSrc + '" alt="">'
			: '<span class="paper-icon paper-icon-lg">' + ICONS.code + '</span>';

		var titleHtml = c.url
			? '<a href="' + c.url + '" target="_blank">' + c.title + '</a>'
			: '<span class="paper-title-text">' + c.title + '</span>';

		var desc = c.description
			? '<div class="paper-meta"><span class="paper-venue">' + c.description + '</span></div>'
			: '';

		li.innerHTML = '<div class="paper-header">' + icon +
			'<div class="paper-info">' + titleHtml + desc + '</div></div>';

		ul.appendChild(li);
	});
}

function _retypeset(el) {
	if (typeof MathJax !== 'undefined' && MathJax.Hub) {
		MathJax.Hub.Queue(['Typeset', MathJax.Hub, el]);
	}
}

function toggleSlowly(elementId) {
	var el = document.getElementById(elementId);
	if (!el) return;

	// Find the button that triggered this toggle
	var btn = document.querySelector('[onclick*="' + elementId + '"]');

	if (el.classList.contains('expanded')) {
		el.style.maxHeight = el.scrollHeight + 'px';
		el.offsetHeight;
		el.style.maxHeight = '0';
		el.classList.remove('expanded');
		if (btn) btn.classList.remove('active');
	} else {
		el.classList.add('expanded');
		el.style.maxHeight = el.scrollHeight + 'px';
		if (btn) btn.classList.add('active');
		var handler = function() {
			el.style.maxHeight = 'none';
			el.removeEventListener('transitionend', handler);
		};
		el.addEventListener('transitionend', handler);
	}
}
