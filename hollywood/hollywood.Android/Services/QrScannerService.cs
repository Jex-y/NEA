using Android.App;
using Android.Content;
using Android.OS;
using Android.Runtime;
using Android.Views;
using Android.Widget;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Xamarin.Forms;


using hollywood.Services;
using ZXing.Mobile;
using ZXing.Net.Mobile.Forms;
using System.Threading;

[assembly: Dependency(typeof(hollywood.Droid.Services.QrScannerService))]
namespace hollywood.Droid.Services
{
    public class QrScannerService : IQrScannerService
    {
        public QrScannerService() 
        {
            
        }
        public async Task<string> readCode()
        {
            // Uses code from https://stackoverflow.com/questions/60059204/await-action-is-not-awaited
            // and https://github.com/Redth/ZXing.Net.Mobile/issues/718

            var options = new MobileBarcodeScanningOptions
            {
                AutoRotate = false,
                UseFrontCameraIfAvailable = false,
                TryHarder = true
            };

            var overlay = new ZXingDefaultOverlay
            {
                TopText = "Please scan QR code",
                BottomText = "Align the QR code within the frame"
            };
            
            var QRScanner = new ZXingScannerPage(options, overlay);

            string Result = null;

            using (SemaphoreSlim semaphore = new SemaphoreSlim(0, 1))
            {

                QRScanner.OnScanResult += (result) =>
                {
                    QRScanner.IsScanning = false;

                    Device.InvokeOnMainThreadAsync(async () =>
                    {
                        await App.Current.MainPage.Navigation.PopModalAsync();
                        try
                        {
                            Result = result.Text;
                        }
                        catch (Exception ex)
                        {
                            Result = ex.Message;
                        }
                        semaphore.Release();
                    });
                };

                await App.Current.MainPage.Navigation.PushModalAsync(QRScanner);
                await semaphore.WaitAsync();
            }

            return Result;
        }
    }
}