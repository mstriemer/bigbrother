xtag.register('x-gravatar', {
    lifecycle: {
        created: function () {
            var img = new Image();
            img.src = this.src;
            img.height = this.size;
            img.width = this.size;
            this.appendChild(img);
        },
    },
    accessors: {
        email: {attribute: 'email'},
        size: {
            get: function () {
                return this.getAttribute('size') || 200;
            },
        },
        hash: {
            get: function () {
                return hex_md5(this.email.toLowerCase());
            },
        },
        src: {
            get: function () {
                return [
                    '//www.gravatar.com/avatar/',
                    this.hash,
                    '?s=',
                    this.size,
                ].join('');
            },
        },
    },
});
