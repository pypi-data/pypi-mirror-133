def main(domain, port, api_key, credentials):
    from omnitools import p
    import userscloud
    import traceback
    import dwa
    if not isinstance(credentials[0], list):
        credentials = [credentials]
    uc_webs = []
    for i, credential in enumerate(credentials):
        p("[pre-start] logging in UC_WEB ({}/{})".format(i+1, len(credentials)))
        uc_web = userscloud.UC_WEB()
        try:
            uc_web.login(credential)
        except:
            traceback.print_exc()
            return
        uc_webs.append(uc_web)
    uc_api = userscloud.UC_API(key=api_key)
    dwa.handlers.BaseResponse.uc_api = uc_api
    dwa.handlers.BaseResponse.uc_webs = uc_webs
    dwa.workers.base_worker.uc_webs = uc_webs
    dwa.workers.base_worker.uc_api = uc_api
    dwa.DWA(domain, port, 365, {"clone_file_private": uc_api.FileClone})
    for i, uc_web in enumerate(uc_webs):
        p("[post-start] logging out UC_WEB ({}/{})".format(i+1, len(uc_webs)))
        try:
            uc_web.logout()
        except:
            pass


