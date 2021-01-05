using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Text;
using System.Threading.Tasks;
using hollywood.Models;

namespace hollywood.Services
{
    public interface IRestService
    {
        Task<Menu> GetMenuAsync(MenuHandle handle);

    }
}
