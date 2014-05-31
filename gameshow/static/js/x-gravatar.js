xtag.register('x-gravatar', {
    lifecycle: {
        created: function () {
            this.img = new Image();
            this.img.src = this.src;
            this.img.height = this.size;
            this.img.width = this.size;
            this.appendChild(this.img);
        },
        attributeChanged: function () {
            this.img.src = this.src;
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
