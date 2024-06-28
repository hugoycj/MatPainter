import click
import json

@click.group()
@click.option('--model_path', '-m', required=True, help='Path to the model file')
@click.option('--output_path', '-o', help='Path to save the output file')
@click.option('--source_path', '-s', help='Path to camera source')
@click.pass_context
def cli(ctx, model_path, output_path, source_path):
    # Load mesh
    from matpainter.mesh import Mesh
    mesh = Mesh.load(model_path)
    
    # Load cameras
    cameras = None
    if source_path is not None:
        print(f"Loading camera data from {source_path}")
        if source_path.endswith('.json'):
            with open(source_path, 'r') as f:
                camera_data = json.load(f)
            cameras = [JSON_to_camera(camera_json, "cuda") for camera_json in camera_data]
        else:
            dataset_config = {
                "name": "colmap",
                "source_path": source_path,
                "images": "images",
                "resolution": -1,
                "data_device": "cuda",
                "eval": False
            }
            dataset = datasets.make(dataset_config)
            cameras = dataset.all_cameras
    
    ctx.ensure_object(dict)
    ctx.obj['mesh'] = mesh
    ctx.obj['cameras'] = cameras
    ctx.obj['output_path'] = output_path

@cli.command()
@click.option('--normal-method', default='stabledenormal', help='Method for normal map generation')
@click.option('--diffuse-method', default='stabledelight', help='Method for diffuse map generation')
@click.option('--pbr-method', default='IntrinsicImageDiffusion', help='Method for PBR map generation')
@click.pass_context
def all(ctx, normal_method, diffuse_method, pbr_method):
    print("Main command execution")
    print(f"Mesh: {ctx.obj['mesh']}")
    print(f"Cameras: {ctx.obj['cameras']}")
    print(f"Output path: {ctx.obj['output_path']}")
    print(f"Normal method: {normal_method}")
    print(f"Diffuse method: {diffuse_method}")
    print(f"PBR method: {pbr_method}")
    # TODO: Implement main logic here

@cli.command()
@click.option('--method', default='StableNormal', help='Method for normal map generation')
@click.pass_context
def normal(ctx, method):
    print("Normal map generation")
    # TODO: Implement normal map generation

@cli.command()
@click.pass_context
@click.option('--method', default='StableDelight', help='Method for diffuse map generation')
def diffuse(ctx, method):
    print("Diffuse map generation")
    # TODO: Implement diffuse map generation

@cli.command()
@click.option('--method', default='IntrinsicImageDiffusion', help='Method for PBR map generation')
@click.pass_context
def pbr(ctx, method):
    print("PBR map generation")
    # TODO: Implement PBR map generation

if __name__ == '__main__':
    cli(obj={})