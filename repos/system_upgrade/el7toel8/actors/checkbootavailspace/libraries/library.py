from os import statvfs

from leapp.libraries.stdlib import api
from leapp.models import Inhibitor

MIN_AVAIL_BYTES_FOR_BOOT = 100 * 2**20  # 100 MiB


def check_avail_space_on_boot(boot_avail_space_getter):
    avail_bytes = boot_avail_space_getter()
    if is_additional_space_required(avail_bytes):
        inhibit_upgrade(avail_bytes)


def get_avail_bytes_on_boot():
    boot_stat = statvfs('/boot')
    return boot_stat.f_frsize * boot_stat.f_bavail


def is_additional_space_required(avail_bytes):
    return avail_bytes < MIN_AVAIL_BYTES_FOR_BOOT


def inhibit_upgrade(avail_bytes):
    additional_mib_needed = (MIN_AVAIL_BYTES_FOR_BOOT - avail_bytes) / 2**20
    api.produce(Inhibitor(
        summary='Not enough space on /boot',
        details='/boot needs additional {0} MiB to be able to accomodate the upgrade initramfs and new kernel.'
                .format(additional_mib_needed)))
