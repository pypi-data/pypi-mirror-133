import re
import uuid
import basehash


class UUIDAPIKey:
    def __init__(self) -> None:
        self._hashfunc = basehash.base36(length=8)

    def check_dashes(self, positions: list, string: str) -> bool:
        test: bool = True

        for pos in positions:
            char = string[pos]
            test = test and (char == '-')

        return test

    def is_uuid(self, uuid: str) -> bool:
        if not bool(uuid):
            raise ReferenceError(
                'The required parameter \'uuid\' is undefined.')

        uuid_check: bool = self.check_dashes([8, 13, 18], uuid)
        uuid = uuid.replace('-', '')

        pattern = re.compile('[a-fA-F0-9]{32}')
        re_check: bool = bool(pattern.match(uuid))

        return uuid_check and re_check and (len(uuid) == 32)

    def is_apikey(self, apikey: str) -> bool:
        if not bool(apikey):
            raise ReferenceError(
                'The required parameter \'apikey\' is undefined.')

        apikey = apikey.upper().replace('-', '')

        pattern = re.compile('[A-Z0-9]{28}')
        re_check: bool = bool(pattern.match(apikey))

        return re_check and (len(apikey) == 32)

    def to_apikey(self, uuid: str, **kwargs):
        no_dash: bool = kwargs.get('no_dash', False)

        if not bool(uuid):
            raise ReferenceError(
                'The required parameter \'uuid\' is undefined.')

        if self.is_uuid(uuid):
            uuid = uuid.replace('-', '')

            s1: str = uuid[0:8]
            s2: str = uuid[8:16]
            s3: str = uuid[16:24]
            s4: str = uuid[24:32]

            n1: int = int(f'0x{s1}', 0)
            n2: int = int(f'0x{s2}', 0)
            n3: int = int(f'0x{s3}', 0)
            n4: int = int(f'0x{s4}', 0)

            e1: str = self._hashfunc.hash(n1)
            e2: str = self._hashfunc.hash(n2)
            e3: str = self._hashfunc.hash(n3)
            e4: str = self._hashfunc.hash(n4)

            if bool(no_dash):
                return f'{e1}{e2}{e3}{e4}'

            return f'{e1}-{e2}-{e3}-{e4}'

        raise TypeError(f'The value provide \'{uuid}\' is not a valid uuid.')

    def to_uuid(self, apikey: str):
        if not bool(apikey):
            raise ReferenceError(
                'The required parameter \'apikey\' is undefined.')

        if self.is_apikey(apikey):
            apikey = apikey.replace('-', '')

            e1: str = apikey[0:8]
            e2: str = apikey[8:16]
            e3: str = apikey[16:24]
            e4: str = apikey[24:32]

            n1: int = self._hashfunc.unhash(e1)
            n2: int = self._hashfunc.unhash(e2)
            n3: int = self._hashfunc.unhash(e3)
            n4: int = self._hashfunc.unhash(e4)

            s1: str = '{0:X}'.format(n1).lower().rjust(8, '0')
            s2: str = '{0:X}'.format(n2).lower().rjust(8, '0')
            s3: str = '{0:X}'.format(n3).lower().rjust(8, '0')
            s4: str = '{0:X}'.format(n4).lower().rjust(8, '0')

            s2a: str = s2[0:4]
            s2b: str = s2[4:8]
            s3a: str = s3[0:4]
            s3b: str = s3[4:8]

            return f'{s1}-{s2a}-{s2b}-{s3a}-{s3b}{s4}'

        raise TypeError(
            f'The value provide \'{apikey}\' is not a valid apikey.')

    def validate(self, apikey: str, uuid: str):
        if not bool(apikey):
            raise ReferenceError(
                'The required parameter \'apikey\' is undefined.')

        if not bool(uuid):
            raise ReferenceError(
                'The required parameter \'uuid\' is undefined.')

        api_check: bool = self.is_apikey(apikey)
        uuid_check: bool = self.is_uuid(uuid)

        if api_check and uuid_check:
            uuid_to_check: str = self.to_uuid(apikey)

            return uuid == uuid_to_check

        err_msg: str = ''

        if not api_check:
            err_msg = err_msg + \
                f'The value provide \'{apikey}\' is not a valid apiKey. '
        if not uuid_check:
            err_msg = err_msg + \
                f'The value provide \'{uuid}\' is not a valid apiKey. '

        raise TypeError(err_msg)

    def generate(self, **kwargs):
        no_dash: bool = kwargs.get('no_dash', False)

        _uuid: str = str(uuid.uuid4())
        _apikey: str = self.to_apikey(_uuid)

        return {'apikey': _apikey, 'uuid': _uuid}
