from dwa import *
import requests
import random


class change_password_worker(workers.once_inverted_base_worker):
    def job(self) -> None:
        fp = os.path.join(self.app_root, "new_password.json")
        if os.path.isfile(fp):
            try:
                pw = json.loads(open(fp, "rb").read().decode())
                if not isinstance(pw, list):
                    raise ValueError("{} is not a list".join(fp))
                if not pw or pw and not isinstance(pw[0], list):
                    raise ValueError("{} is not a list of lists".join(fp))
                self.sql(
                    '''
                    UPDATE `owners`
                    SET `hash` = ?
                    WHERE `name` = ?;
                    ''',
                    tuple([tuple(_) for _ in pw])
                )
            except:
                traceback.print_exc()
            os.remove(fp)
        print("[workers] change_password_worker: done")


class dummy_api_worker(workers.once_inverted_base_worker):
    api_keys_fp = None

    def job(self) -> None:
        import userscloud
        self.export_functions = {
            "get_dummy_api": self.get_dummy_api,
            "clone_file_public": lambda x: userscloud.UC_API(key=self.get_dummy_api()).FileClone(x),
        }
        fp = os.path.join(self.app_root, "dummy_api.txt")
        if os.path.isfile(fp):
            _fp = open(fp, "rb").read().decode()
            os.remove(fp)
            if os.path.isfile(_fp):
                self.api_keys_fp = _fp
        print("[workers] dummy_api_worker: done")

    def get_dummy_api(self):
        if self.api_keys_fp:
            try:
                api_keys = json.loads(open(self.api_keys_fp, "rb").read().decode())
                if not isinstance(api_keys, list):
                    raise ValueError("{} is not a list".join(self.api_keys_fp))
            except:
                traceback.print_exc()
                return
            if api_keys:
                import random
                return random.SystemRandom().choice(api_keys)
            else:
                return
        else:
            return


class renew_code_worker(workers.base_worker):
    pending = 0

    def job(self) -> None:
        r = self.sql(
            '''
            SELECT `code`, `id`
            FROM `files`
            WHERE DATETIME('NOW', 'LOCALTIME') >= DATETIME(`date`, '+21 days')
            LIMIT 1;
            ''',
            (),
            "list"
        )
        if r:
            if not self.pending:
                self.pending = self.sql(
                    '''
                    SELECT COUNT(*)
                    FROM `files`
                    WHERE DATETIME('NOW', 'LOCALTIME') >= DATETIME(`date`, '+21 days');
                    ''',
                    (),
                    "list"
                )[0][0]
            code, id = r[0]
            try:
                print("\rpending: {} items left".format(self.pending), end="", flush=True)
                result = self.uc_api.FileClone(code)["result"]["filecode"]
                data = (result, id)
                self.sql(
                    '''
                    UPDATE `files`
                    SET `code` = ?
                    WHERE `id` = ?;
                    ''',
                    data
                )
                self.pending -= self.pending
                if not self.pending:
                    print(flush=True)
                return
            except:
                pass
        time.sleep(1)


class gen_sitemap_worker(workers.inverted_base_worker):
    def job(self) -> None:
        r = self.sql(
            '''
            SELECT `id`
            FROM `folders`
            WHERE `public`;
            ''',
            (),
            "list"
        )
        def loop_folder(id):
            r = self.sql(
                '''
                SELECT `id`
                FROM `folders`
                WHERE `parent` = ?;
                ''',
                (id,),
                "list"
            )
            for _ in r:
                loop_folder(_[0])
            r = self.sql(
                '''
                SELECT `id`, `name`
                FROM `files`
                WHERE `parent` = ?
                AND LENGTH(`name`) = 44
                AND `name` LIKE "%.zip";
                ''',
                (id,),
                "list"
            )
            [sitemap.append(_[0]) for _ in r if _[0] not in sitemap and re.search(r"^[a-zA-Z0-9]{40}\.zip$", _[1])]
        sitemap = []
        for _ in r:
            id = _[0]
            loop_folder(id)
        xml = '''<?xml version="1.0" encoding="UTF-8"?>'''
        xml += '''<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'''
        url = '''
    <url>
        <loc>{}/{{}}</loc>
        <priority>{{}}</priority>
    </url>'''.format("http://"+self.cookies_domain[1:])
        for _ in sitemap:
            xml += url.format(_, "1.0")
        xml += '''</urlset>'''
        open(os.path.join(self.app_root, "root", "sitemap.xml"), "wb").write(xml.encode())
        print("[workers] gen_sitemap_worker: done")



