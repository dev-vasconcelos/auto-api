using System;
using System.Linq;
using System.Collections.Generic;
//using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Http;
using ${projectName}.Models;
using ${projectName}.DataBase;
using ${projectName}.Service.AbstractClass;
using ${projectName}.DTO.AbstractClass;
using ${projectName}.Controllers.Interface;
using ${projectName}.Response;
using Microsoft.AspNetCore.Authorization;
using ${projectName}.Service.Models.Interface;

namespace ${projectName}.Controllers.AbstractClass
{
    [ApiController]
    // [Authorize]
    [Produces("application/json")]
    [Route("api/[controller]")]
    public abstract class AbstractController<T, DTO> : ControllerBase, IController<T, DTO> where T : AbstractEntity where DTO : AbstractModelDTO<T, DTO>
    {

        protected AbstractServiceNpgsql<T> _service;
        protected NpgContext _contexto;
        protected Microsoft.Extensions.Configuration.IConfiguration _configuration { get; }
        // protected Models.Usuario _User => new AbstractServiceNpgsql<Usuario>(_contexto).Get(x => x.UserKey.Equals(this.GetUserKey()), new string[] { "Scope" }).FirstOrDefault();

        public AbstractController(NpgContext contexto, Microsoft.Extensions.Configuration.IConfiguration configuration)
        {
            _configuration = configuration;
            this._contexto = contexto;
            this._service = new AbstractServiceNpgsql<T>(contexto);
        }

        public AbstractController(NpgContext contexto)
        {
            this._contexto = contexto;
            this._service = new AbstractServiceNpgsql<T>(contexto);
        }

        [HttpGet]
        [Route("fromquery")]
        [ProducesDefaultResponseType]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status204NoContent)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        [ProducesResponseType(StatusCodes.Status500InternalServerError)]
        [ProducesResponseType(StatusCodes.Status501NotImplemented)]
        public abstract IActionResult GetFromQuery([FromQuery] string term);


        [HttpGet]
        [ProducesDefaultResponseType]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status204NoContent)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        [ProducesResponseType(StatusCodes.Status500InternalServerError)]
        [ProducesResponseType(StatusCodes.Status501NotImplemented)]
        public virtual IActionResult Get()
        {
            ResponseEntity<IEnumerable<T>> response;

            try
            {
                // response = new ResponseEntity<IEnumerable<T>>(_service.Get(x => x.ScopeId == _User.ScopeId));
                response = new ResponseEntity<IEnumerable<T>>(_service.Get());

            }
            catch (Exception ex)
            {
                response = new ResponseEntity<IEnumerable<T>>(new List<T>(), ex);
                return StatusCode(500, response);
            }

            return Ok(response);
        }

        [HttpPost]
        [ProducesDefaultResponseType]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status204NoContent)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        [ProducesResponseType(StatusCodes.Status500InternalServerError)]
        [ProducesResponseType(StatusCodes.Status501NotImplemented)]
        public virtual IActionResult Post([FromBody] DTO dto)
        {
            ResponseEntity<T> response;

            var entity = dto.ConvertFromDto(dto); //if id in relationship add
            // entity.ScopeId = _User.ScopeId;

            try
            {
                entity = Checker(entity);

                _service.Save(entity);
            }
            catch (NullReferenceException)
            {
                response = new ResponseEntity<T>(entity, "Informações nulas");
                return StatusCode(500, response);
            }
            catch (ArgumentNullException ex)
            {
                response = new ResponseEntity<T>(entity, ex.Message);
                return StatusCode(500, response);
            }
            catch (Exception ex)
            {
                response = new ResponseEntity<T>(entity, ex);
                return StatusCode(500, response);
            }

            response = new ResponseEntity<T>(entity);
            return Ok(response);
        }

        [HttpGet("{property}/{value}")]
        [ProducesDefaultResponseType]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status204NoContent)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        [ProducesResponseType(StatusCodes.Status500InternalServerError)]
        [ProducesResponseType(StatusCodes.Status501NotImplemented)]
        public virtual IActionResult Get(string property, string value)
        {
            throw new NotImplementedException();
        }

        [HttpGet("{id}")]
        [ProducesDefaultResponseType]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status204NoContent)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        [ProducesResponseType(StatusCodes.Status500InternalServerError)]
        [ProducesResponseType(StatusCodes.Status501NotImplemented)]
        public virtual IActionResult Get(long id)
        {
            ResponseEntity<DTO> response;


            T entity = (T)Activator.CreateInstance(typeof(T));
            DTO dto = (DTO)Activator.CreateInstance(typeof(DTO));
            try
            {
                // entity = _service.Get(x => x.Id == id).FirstOrDefault(); //pq tava usando esse ao inves do id pedro?

                entity = _service.Get(id);

                dto = dto.ConvertToDto<T, DTO>(entity);

            }
            catch (InvalidOperationException)
            {
                response = new ResponseEntity<DTO>(dto.ConvertToDto<T, DTO>(entity), "Id duplicado");
                return StatusCode(500, response);
            }
            catch (Exception ex)
            {
                response = new ResponseEntity<DTO>(dto.ConvertToDto<T, DTO>(entity), ex);
                return StatusCode(500, response);
            }

            if (entity == null)
            {
                response = new ResponseEntity<DTO>(dto.ConvertToDto<T, DTO>(entity), typeof(T).Name + " não encontrado");
                return Ok(response);
            }

            response = new ResponseEntity<DTO>(dto.ConvertToDto<T, DTO>(entity));

            return Ok(response);
        }

        [HttpPut]
        [ProducesDefaultResponseType]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status204NoContent)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        [ProducesResponseType(StatusCodes.Status500InternalServerError)]
        [ProducesResponseType(StatusCodes.Status501NotImplemented)]
        public virtual IActionResult Put([FromBody] DTO dto)
        {
            ResponseEntity<T> response;
            var entity = dto.ConvertFromDto(dto);

            if (entity.Id.Equals(null))
            {
                response = new ResponseEntity<T>(entity, "ID nulo");
                BadRequest(response);
            }

            try
            {
                _service.Update(entity);

            }
            catch (Exception ex)
            {
                response = new ResponseEntity<T>(entity, ex);
                return StatusCode(500, response);
            }

            response = new ResponseEntity<T>(entity);
            return Ok(response);
        }

        //[NonAction]
        [HttpDelete("{id}")]
        [ProducesDefaultResponseType]
        [ProducesResponseType(StatusCodes.Status200OK)]
        [ProducesResponseType(StatusCodes.Status204NoContent)]
        [ProducesResponseType(StatusCodes.Status400BadRequest)]
        [ProducesResponseType(StatusCodes.Status404NotFound)]
        [ProducesResponseType(StatusCodes.Status500InternalServerError)]
        [ProducesResponseType(StatusCodes.Status501NotImplemented)]
        public virtual IActionResult Delete(long id)
        {
            ResponseEntity<T> response;

            T entity = (T)Activator.CreateInstance(typeof(T));
            entity.Id = id;

            try
            {
                _service.Delete(entity);
            }
            catch (ArgumentNullException)
            {
                response = new ResponseEntity<T>(entity, "Não existe");
                return StatusCode(500, response);
            }
            catch (InvalidOperationException ex)
            {
                response = new ResponseEntity<T>(entity, ex);
                return BadRequest(response);
            }
            catch (Exception ex)
            {
                response = new ResponseEntity<T>(entity, ex);
                return StatusCode(500, response);
            }
            response = new ResponseEntity<T>(entity);
            return Ok(response);
        }

        private T Checker(T generic)
        {
            foreach (var i in generic.GetType().GetProperties().ToList())
            {
                if (generic.GetType().GetProperty(i.Name).GetValue(generic) is AbstractEntity)
                {
                    dynamic a = Activator.CreateInstance(generic.GetType().GetProperty(i.Name).PropertyType);
                    a = generic.GetType().GetProperty(i.Name).GetValue(generic);
                    if (a.Id != 0) // Se não encontrar ID, adicionar
                    {
                        a = getTheGenericOneBitch(a);
                        generic.GetType().GetProperty(i.Name).SetValue(generic, a);
                    }
                }
            }
            return generic;
        }

        private T GetChain(T generic) => throw new NotImplementedException(); //Em algum print

        private T2 getTheGenericOneBitch<T2>(T2 algo) where T2 : AbstractEntity
        {
            AbstractServiceNpgsql<T2> genericService = new AbstractServiceNpgsql<T2>(_contexto);
            return genericService.Get(algo);
        }

        /* User key fica aqui kk */
    }

}
