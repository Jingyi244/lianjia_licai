var page = require('webpage').create();
var fs = require('fs');
page.open('https://licai.lianjia.com/licai', function () {
        page.evaluate(function(){
                });
});
page.onLoadFinished = function() {
     console.log("page load finished");
     page.render('licai.png');
     fs.write('licai.html', page.content, 'w');
     phantom.exit();
};

