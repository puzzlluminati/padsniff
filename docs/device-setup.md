# Device Setup

`padsniff run` will generate a root key and certificate on first run, and place them in `~/.padsniff` by default. To use padsniff's proxying capabilities, you'll need to install the generated root pair to your device.

## Security

The root pair is dynamically generated and will be different for every installation. It's very important not to give out the key (`padsniff-ca-key.pem` and the first half of `padsniff-ca.pem`), as once the certificate (`padsniff-ca-cert.pem`) is installed on your device it will trust any leaf certificate signed with this key, which can leave you open to a malicious attacker.

## Android (< 7.0)

You will need to set up a lock screen to use user-supplied credentials. If you'd like to avoid this, see the [Android (7.0+) section](#Android (7.0+)).

- Locate your combined root CA credentials. (default: `~/.padsniff/padsniff-ca.pem`)
- Copy this file to your device.
- Open the Security settings and choose "Install from storage".
- Locate and choose the `padsniff-ca.pem` file.
- Give the credentials a name and, if prompted, choose "VPN and apps" for use.
- Verify the credentials can be found in Security > Trusted credentials > User.

## Android (7.0+)

**Your device must be rooted to use this method.**

Prior to Android 7.0 (Nougat), apps would trust both the user-supplied and system certificate stores. Nougat introduced a breaking change to apps' default network security config to only trust the system certificate store. Unfortunately many apps, PAD included, don't modify this default behavior, and as of PAD v12.2 the target SDK version has been bumped to 24 (7.0 Nougat), breaking standard `padsniff` setups that depend on a user-supplied trusted certificate to re-sign traffic. Android devices below version 7.0 are not subject to this behavior.

- Locate your combined root CA credentials. (default: `~/.padsniff/padsniff-ca.pem`)
- Compute the legacy hash of this file.

```shell
$ # openssl version >= 1.0.0
$ HASH=$(openssl x509 -inform PEM -subject_hash_old -in padsniff-ca.pem | head -1)
$ # < 1.0.0
$ HASH=$(openssl x509 -inform PEM -subject_hash -in padsniff-ca.pem | head -1)
```

- Copy the cert to your device at `/system/etc/security/cacerts/${HASH}.0` and set permissions to `644`. You can do this on your device with a file manager that has root access, or through `adb`.

```shell
$ sudo adb start-server
* daemon not running. starting it now on port 5037 *
* daemon started successfully *
$ adb push padsniff-ca.pem "/sdcard/${HASH}.0"
[100%] /sdcard/<filename>
$ adb shell
device:/ $ # this will probably ask for root access on your device
device:/ $ su
device:/ # mount -o remount,rw /system
device:/ # # this shell doesn't contain our environment variable above
device:/ # # so be sure to manually substitute the filename
device:/ # mv /sdcard/<filename> /system/etc/security/cacerts/
device:/ # chmod 644 /system/etc/security/cacerts/<filename>
device:/ # mount -o remount,ro /system
device:/ # exit
device:/ $ exit
```

- Reboot your device.
- Confirm the certificate is installed under Settings > Security > Trusted Credentials > System. If using the default settings it will be named "Puzzle & Dragons HTTP Sniffer".

## iOS

The creator of padsniff doesn't own an iOS device, and thus is unfortunately unable to write an accurate guide for installing credentials to iOS devices, or speak of the validity of other such guides.

If you've gotten padsniff working on your iOS device, please submit a pull request documenting the steps you took to get there!
