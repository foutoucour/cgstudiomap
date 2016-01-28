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
            'paper-clip': '&#xe001;',
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
            'air-play': '&#xe016;',
            'camera': '&#xe017;',
            'video': '&#xe018;',
            'disc': '&#xe019;',
            'printer': '&#xe020;',
            'monitor': '&#xe021;',
            'server': '&#xe022;',
            'cog': '&#xe023;',
            'heart': '&#xe024;',
            'paragraph': '&#xe025;',
            'align-justify': '&#xe026;',
            'align-left': '&#xe027;',
            'align-center': '&#xe028;',
            'align-right': '&#xe029;',
            'book': '&#xe030;',
            'layers': '&#xe031;',
            'stack': '&#xe032;',
            'stack-2': '&#xe033;',
            'paper': '&#xe034;',
            'paper-stack': '&#xe035;',
            'search': '&#xe036;',
            'zoom-in': '&#xe037;',
            'zoom-out': '&#xe038;',
            'reply': '&#xe039;',
            'circle-plus': '&#xe040;',
            'circle-minus': '&#xe041;',
            'circle-check': '&#xe042;',
            'circle-cross': '&#xe043;',
            'square-plus': '&#xe044;',
            'square-minus': '&#xe045;',
            'square-check': '&#xe046;',
            'square-cross': '&#xe047;',
            'microphone': '&#xe048;',
            'record': '&#xe049;',
            'skip-back': '&#xe050;',
            'rewind': '&#xe051;',
            'play': '&#xe052;',
            'pause': '&#xe053;',
            'stop': '&#xe054;',
            'fast-forward': '&#xe055;',
            'skip-forward': '&#xe056;',
            'shuffle': '&#xe057;',
            'repeat': '&#xe058;',
            'folder': '&#xe059;',
            'umbrella': '&#xe060;',
            'moon': '&#xe061;',
            'thermometer': '&#xe062;',
            'drop': '&#xe063;',
            'sun': '&#xe064;',
            'cloud': '&#xe065;',
            'cloud-upload': '&#xe066;',
            'cloud-download': '&#xe067;',
            'upload': '&#xe068;',
            'download': '&#xe069;',
            'location': '&#xe070;',
            'location-2': '&#xe071;',
            'map': '&#xe072;',
            'battery': '&#xe073;',
            'head': '&#xe074;',
            'briefcase': '&#xe075;',
            'speed-bubble': '&#xe076;',
            'anchor': '&#xe077;',
            'globe': '&#xe078;',
            'box': '&#xe079;',
            'reload': '&#xe080;',
            'share': '&#xe081;',
            'marquee': '&#xe082;',
            'marquee-plus': '&#xe083;',
            'marquee-minus': '&#xe084;',
            'tag': '&#xe085;',
            'power': '&#xe086;',
            'command': '&#xe087;',
            'alt': '&#xe088;',
            'esc': '&#xe089;',
            'bar-graph': '&#xe090;',
            'bar-graph-2': '&#xe091;',
            'pie-graph': '&#xe092;',
            'star': '&#xe093;',
            'arrow-left': '&#xe094;',
            'arrow-right': '&#xe095;',
            'arrow-up': '&#xe096;',
            'arrow-down': '&#xe097;',
            'volume': '&#xe098;',
            'mute': '&#xe099;',
            'content-right': '&#xe100;',
            'content-left': '&#xe101;',
            'grid': '&#xe102;',
            'grid-2': '&#xe103;',
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
            'file-add': '&#xe125;',
            'file-substract': '&#xe126;',
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
