/* A polyfill for browsers that don't support ligatures. */
/* The script tag referring to this file must be placed before the ending body tag. */

/* To provide support for elements dynamically added, this script adds
   method 'icomoonLiga' to the window object. You can pass element references to this method.
*/
(function () {
    'use strict';
    function supportsProperty(p) {
        var prefixes = ['Webkit', 'Moz', 'O', 'ms'],
            i,
            div = document.createElement('div'),
            ret = p in div.style;
        if (!ret) {
            p = p.charAt(0).toUpperCase() + p.substr(1);
            for (i = 0; i < prefixes.length; i += 1) {
                ret = prefixes[i] + p in div.style;
                if (ret) {
                    break;
                }
            }
        }
        return ret;
    }
    var icons;
    if (!supportsProperty('fontFeatureSettings')) {
        icons = {
            'facebook': '&#xe900;',
            'github': '&#xe901;',
            'instagram': '&#xe902;',
            'linkedin': '&#xe903;',
            'twitter': '&#xe906;',
            'vimeo': '&#xe907;',
            'youtube': '&#xe908;',
            'eye': '&#xe000;',
            'paperClip': '&#xe001;',
            'mail': '&#xe002;',
            'toggle': '&#xe003;',
            'layout': '&#xe004;',
            'link': '&#xe005;',
            'bell': '&#xe006;',
            'lock': '&#xe007;',
            'unlock': '&#xe008;',
            'ribbon': '&#xe009;',
            'image': '&#xe010;',
            'signal': '&#xe011;',
            'target': '&#xe012;',
            'clipboard': '&#xe013;',
            'clock': '&#xe014;',
            'watch': '&#xe015;',
            'airPlay': '&#xe016;',
            'camera': '&#xe017;',
            'video': '&#xe018;',
            'disc': '&#xe019;',
            'printer': '&#xe020;',
            'monitor': '&#xe021;',
            'server': '&#xe022;',
            'cog': '&#xe023;',
            'heart': '&#xe024;',
            'paragraph': '&#xe025;',
            'alignJustify': '&#xe026;',
            'alignLeft': '&#xe027;',
            'alignCenter': '&#xe028;',
            'alignRight': '&#xe029;',
            'book': '&#xe030;',
            'layers': '&#xe031;',
            'stack': '&#xe032;',
            'stack2': '&#xe033;',
            'paper': '&#xe034;',
            'paperStack': '&#xe035;',
            'search': '&#xe036;',
            'zoomIn': '&#xe037;',
            'zoomOut': '&#xe038;',
            'reply': '&#xe039;',
            'circlePlus': '&#xe040;',
            'circleMinus': '&#xe041;',
            'circleCheck': '&#xe042;',
            'circleCross': '&#xe043;',
            'squarePlus': '&#xe044;',
            'squareMinus': '&#xe045;',
            'squareCheck': '&#xe046;',
            'squareCross': '&#xe047;',
            'microphone': '&#xe048;',
            'record': '&#xe049;',
            'skipBack': '&#xe050;',
            'rewind': '&#xe051;',
            'play': '&#xe052;',
            'pause': '&#xe053;',
            'stop': '&#xe054;',
            'fastForward': '&#xe055;',
            'skipForward': '&#xe056;',
            'shuffle': '&#xe057;',
            'repeat': '&#xe058;',
            'folder': '&#xe059;',
            'umbrella': '&#xe060;',
            'moon': '&#xe061;',
            'thermometer': '&#xe062;',
            'drop': '&#xe063;',
            'sun': '&#xe064;',
            'cloud': '&#xe065;',
            'cloudUpload': '&#xe066;',
            'cloudDownload': '&#xe067;',
            'upload': '&#xe068;',
            'download': '&#xe069;',
            'location': '&#xe070;',
            'location2': '&#xe071;',
            'map': '&#xe072;',
            'battery': '&#xe073;',
            'head': '&#xe074;',
            'briefcase': '&#xe075;',
            'speedBubble': '&#xe076;',
            'anchor': '&#xe077;',
            'globe': '&#xe078;',
            'box': '&#xe079;',
            'reload': '&#xe080;',
            'share': '&#xe081;',
            'marquee': '&#xe082;',
            'marqueePlus': '&#xe083;',
            'marqueeMinus': '&#xe084;',
            'tag': '&#xe085;',
            'power': '&#xe086;',
            'command': '&#xe087;',
            'alt': '&#xe088;',
            'esc': '&#xe089;',
            'barGraph': '&#xe090;',
            'barGraph2': '&#xe091;',
            'pieGraph': '&#xe092;',
            'star': '&#xe093;',
            'arrowLeft': '&#xe094;',
            'arrowRight': '&#xe095;',
            'arrowUp': '&#xe096;',
            'arrowDown': '&#xe097;',
            'volume': '&#xe098;',
            'mute': '&#xe099;',
            'contentRight': '&#xe100;',
            'contentLeft': '&#xe101;',
            'grid': '&#xe102;',
            'grid2': '&#xe103;',
            'columns': '&#xe104;',
            'loader': '&#xe105;',
            'bag': '&#xe106;',
            'ban': '&#xe107;',
            'flag': '&#xe108;',
            'trash': '&#xe109;',
            'expand': '&#xe110;',
            'contract': '&#xe111;',
            'maximize': '&#xe112;',
            'minimize': '&#xe113;',
            'plus': '&#xe114;',
            'minus': '&#xe115;',
            'check': '&#xe116;',
            'cross': '&#xe117;',
            'move': '&#xe118;',
            'delete': '&#xe119;',
            'menu': '&#xe120;',
            'archive': '&#xe121;',
            'inbox': '&#xe122;',
            'outbox': '&#xe123;',
            'file': '&#xe124;',
            'fileAdd': '&#xe125;',
            'fileSubstract': '&#xe126;',
            'help': '&#xe127;',
            'open': '&#xe128;',
            'ellipsis': '&#xe129;',
          '0': 0
        };
        delete icons['0'];
        window.icomoonLiga = function (els) {
            var classes,
                el,
                i,
                innerHTML,
                key;
            els = els || document.getElementsByTagName('*');
            if (!els.length) {
                els = [els];
            }
            for (i = 0; ; i += 1) {
                el = els[i];
                if (!el) {
                    break;
                }
                classes = el.className;
                if (/cgsm-icon-/.test(classes)) {
                    innerHTML = el.innerHTML;
                    if (innerHTML && innerHTML.length > 1) {
                        for (key in icons) {
                            if (icons.hasOwnProperty(key)) {
                                innerHTML = innerHTML.replace(new RegExp(key, 'g'), icons[key]);
                            }
                        }
                        el.innerHTML = innerHTML;
                    }
                }
            }
        };
        window.icomoonLiga();
    }
}());
