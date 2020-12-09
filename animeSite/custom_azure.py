from storages.backends.azure_storage import AzureStorage


class AzureMediaStorage(AzureStorage):
    # Must be replaced by your <storage_account_name>
    account_name = 'djangoforumstorage'
    # Must be replaced by your <storage_account_key>
    account_key = 'A0IJMHx6zGVzovSqRMwK1nFWU0Nw1wu66nMYNwz4SjY38WqyZcbZvvTApuyzGFfqb2ltkosuMEGQ1hrJWD6azg=='
    azure_container = 'media'
    expiration_secs = None


class AzureStaticStorage(AzureStorage):
    # Must be replaced by your storage_account_name
    account_name = 'djangoforumstorage'
    # Must be replaced by your <storage_account_key>
    account_key = 'A0IJMHx6zGVzovSqRMwK1nFWU0Nw1wu66nMYNwz4SjY38WqyZcbZvvTApuyzGFfqb2ltkosuMEGQ1hrJWD6azg=='
    azure_container = 'static'
    expiration_secs = None
