// discover_widgets.js

// Helper function: Generate an XPath for an element.
function getElementXPath(elt) {
  var path = "";
  for (; elt && elt.nodeType === 1; elt = elt.parentNode) {
      var idx = getElementIdx(elt);
      var xname = elt.tagName.toLowerCase();
      if (idx > 1) {
          xname += "[" + idx + "]";
      }
      path = "/" + xname + path;
  }
  return path;
}

// Helper function: Get the index of an element among its same-tag siblings.
function getElementIdx(elt) {
  var count = 1;
  for (var sib = elt.previousSibling; sib; sib = sib.previousSibling) {
      if (sib.nodeType === 1 && sib.tagName === elt.tagName) {
          count++;
      }
  }
  return count;
}

// Helper function: Generate a CSS selector for an element.
function getElementCSSPath(el) {
  if (!(el instanceof Element))
      return;
  var path = [];
  while (el.nodeType === Node.ELEMENT_NODE) {
      var selector = el.nodeName.toLowerCase();
      if (el.id) {
          selector += '#' + el.id;
          path.unshift(selector);
          break;
      } else {
          var sib = el, nth = 1;
          while (sib = sib.previousElementSibling) {
              if (sib.nodeName.toLowerCase() === selector) nth++;
          }
          if (nth != 1) {
              selector += ":nth-of-type(" + nth + ")";
          }
      }
      path.unshift(selector);
      el = el.parentNode;
  }
  return path.join(" > ");
}



function discoverWidgets() {
  // Select candidate elements – adjust the selector as needed.
  var elements = document.querySelectorAll("a, button, input, select, textarea");
  
  // Filter only visible elements.
  var visibleElements = Array.prototype.filter.call(elements, function(el) {
    var rect = el.getBoundingClientRect();
    return rect.width > 0 && rect.height > 0 &&
           window.getComputedStyle(el).visibility !== 'hidden';
  });
  
  var results = [];
  
  visibleElements.forEach(function(el, index) {
    var rect = el.getBoundingClientRect();
    var widget = {};
    
    // Basic information about the element.
    widget.widget_id = index + 1;
    widget.tag = el.tagName;
    widget.text = el.textContent ? el.textContent.trim() : "";
    widget.x = Math.round(rect.left);
    widget.y = Math.round(rect.top);
    widget.width = Math.round(rect.width);
    widget.height = Math.round(rect.height);
    
    // Now collect locator outputs from your locator_functions.js.
    // (Make sure these functions are defined in locator_functions.js.)
    // widget.xPath = (typeof getXPath === "function") ? getXPath(el) : "";
    // widget.idXPath = (typeof getIdXPath === "function") ? getIdXPath(el) : "";
    // widget.monotoXPath = (typeof getMonotoXPath === "function") ? getMonotoXPath(el) : "";
    // widget.robulaXPath = (typeof getRobulaPlusXPath === "function") ? getRobulaPlusXPath(el) : "";
    // widget.seleniumLocator = (typeof getSeleniumIDELocator === "function") ? getSeleniumIDELocator(el) : "";
    
    // --- 8 Locators ---

    // 1. ID Locator:
    widget.locator_id = el.id || "0";

    // 2. Name Locator:
    widget.locator_name = el.getAttribute("name") || "0";

    // 3. Class Name Locator:
    widget.locator_class = el.className || "0";

    // 4. Tag Name Locator:
    widget.locator_tag = el.tagName;  // same as widget.tag

    // 5 & 6. Link Text and Partial Link Text (only applicable if the element is a link)
    if (el.tagName.toLowerCase() === "a") {
        widget.locator_linkText = el.textContent ? el.textContent.trim() : "";
        widget.locator_partialLinkText = (el.textContent ? el.textContent.trim() : "").substring(0, 10);
    } else {
        widget.locator_linkText = "";
        widget.locator_partialLinkText = "";
    }

    // 7. XPath Locator:
    widget.locator_xpath = getElementXPath(el);

    // 8. CSS Selector Locator:
    widget.locator_css = getElementCSSPath(el);


    results.push(widget);
  });
  
  return results;
}

return discoverWidgets();
