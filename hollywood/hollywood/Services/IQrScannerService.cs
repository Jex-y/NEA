using System;
using System.Collections.Generic;
using System.Text;
using System.Threading.Tasks;

namespace hollywood.Services
{
    public interface IQrScannerService
    {
        Task<string> readCode();
    }
}
