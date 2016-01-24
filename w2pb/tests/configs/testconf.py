from w2p.classes.actions.action import Action


config = {
    'comments': [
        {
            Action.DATA: {
                Action.AD_URL: "http://geektimes.ru/post/267524/"
            },
            Action.TYPE: Action.AT_FAST_DOWNLOAD,
            Action.NAME: "article"
        },
        {
            Action.TYPE: Action.AT_PARSE_BY_SELECTOR,
            Action.NAME: 'something',
            Action.DATA: {
                Action.AD_SELECTOR: 'h1.title .post_title'
            },
            Action.TARGET: ':article.result:',
            Action.SETTINGS: {
                Action.AS_VISIBLE: True
            }
        }
    ]
}
