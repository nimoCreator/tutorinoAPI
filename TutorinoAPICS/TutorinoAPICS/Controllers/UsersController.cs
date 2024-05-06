using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Newtonsoft.Json;
using System.Data;
using System.Data.SqlClient;
using System.Reflection.Metadata.Ecma335;
using TutorinoAPICS.Models;

namespace TutorinoAPICS.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class UsersController : ControllerBase
    {
        public readonly IConfiguration configuration;
        public UsersController(IConfiguration configuration)
        {
            this.configuration = configuration;
        }

        //Test API to retrieve data about users in database
        [HttpGet]
        [Route("getAllUsers")]
        public String GetUsers()
        {
            SqlConnection con = new SqlConnection(configuration.GetConnectionString("UsersAppCon").ToString());
            SqlDataAdapter data = new SqlDataAdapter("Select * from users", con);
            DataTable dataTable = new DataTable();
            data.Fill(dataTable);
            List<User> users = new List<User>();
            Response response = new Response();
            if (dataTable.Rows.Count > 0)
            {
                for (int i = 0; i < dataTable.Rows.Count; i++)
                {
                    User usr = new User();
                    usr.Id = Convert.ToInt32(dataTable.Rows[i]["uuid"]);
                    usr.UserName = Convert.ToString(dataTable.Rows[i]["name"]);
                    usr.UserSurname = Convert.ToString(dataTable.Rows[i]["surname"]);
                    users.Add(usr);
                }
            }
            if(users.Count>0)
            {
                return JsonConvert.SerializeObject(users);
            }
            else
            {
                return JsonConvert.SerializeObject(response);
            }
        }

        //Response codes: 0 - User Added to Database, 102 - User with given mail or login exists in database, 100 - other error
        [HttpPost]
        [Route("addUser")]
        public String AddUser(UserAdded newUser)
        {
            SqlConnection con = new SqlConnection(configuration.GetConnectionString("UsersAppCon").ToString());
            SqlCommand cmd = new SqlCommand("Insert into users(name,surname,login,email,password) values('" + newUser.UserName + "','" + newUser.UserSurname + "','" + newUser.UserLogin + "','" + newUser.UserEmail + "','" + newUser.UserPassword + "')", con);
            con.Open();
            int i;
            try
            {
                i = cmd.ExecuteNonQuery();
            } catch (Exception ex)
            {
                return JsonConvert.SerializeObject(new Response(102, "Data Exists"));
            }
            con.Close();
            if (i > 0)
            {
                return JsonConvert.SerializeObject(new Response(0, "Data added"));
            }
            else
            {
                return JsonConvert.SerializeObject(new Response());
            }
        }

        //Status codes: 0 - Gives access, provided data are correct. 101 - Wrong Password given. 100 - No user with given mail or login in database.
        [HttpPost]
        [Route("loginUser")]
        public String LogUser(UserLogin userData)
        {
            SqlConnection con = new SqlConnection(configuration.GetConnectionString("UsersAppCon").ToString());
            SqlDataAdapter data = new SqlDataAdapter("Select * from users where login = '" + userData.Username + "' or password = '" + userData.Email + "'", con);
            DataTable dataTable = new DataTable();
            data.Fill(dataTable);
            if (dataTable.Rows.Count > 0)
            {
                if (Convert.ToString(dataTable.Rows[0]["password"]) == userData.Password)
                {
                    return JsonConvert.SerializeObject(new Response(0, "Access"));
                }
                else
                {
                    return JsonConvert.SerializeObject(new Response(101, "Wrong Password"));
                }
            }
            else
            {
                return JsonConvert.SerializeObject(new Response(100, "No User"));
            }
        }
    }
}
