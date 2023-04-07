class LaURL:
    def __init__(self, url):
        self.url = url
        __url_split = url.split("/")
        self.protocol = __url_split[0][:-1]
        self.domain = __url_split[2]
        self.full_slug = __url_split[-1]
        self.slug = __url_split[-1].replace("hentai-", "")

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)


class LaHentai:
    def __init__(
            self,
            parse_url,
            count,
            title,
            genres,
            chapters
    ):
        self.parse_url = LaURL(parse_url)
        self.count = len(count)
        self.title = title
        self.genres = list(genres)
        self.chapters = chapters

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)


class LaInfoH:
    def __init__(
            self,
            title,
            url,
            thumb
    ):
        self.title = title
        self.url = url
        self.thumb = thumb

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)


class LaInfo(LaInfoH):
    def __init__(
            self,
            title,
            url,
            chapter_url,
            thumb,
            episode
    ):
        super().__init__(title, url, thumb)
        self.chapter_url = chapter_url
        self.episode = episode

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self.__dict__)
