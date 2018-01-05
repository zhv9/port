let util = {

};
util.title = function (title) {
    title = title ? title + ' - Home' : 'assert project';
    window.document.title = title;
};

export default util;